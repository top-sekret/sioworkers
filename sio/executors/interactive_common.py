import fcntl
import os
import random
import traceback
from shutil import rmtree
from threading import Thread

from sio import feedback
from sio.executors.common import _extract_input_if_zipfile, _populate_environ
from sio.workers import ft
from sio.workers.executors import DetailedUnprotectedExecutor
from sio.workers.util import TemporaryCwd, replace_invalid_UTF, tempcwd
from sio.workers.file_runners import get_file_runner

import signal
import six

DEFAULT_INTERACTOR_MEM_LIMIT = 256 * 1024  # in KiB
RESULT_STRING_LENGTH_LIMIT = 1024  # in bytes


def set_inheritable(fd, inheritable):
    if hasattr(os, 'O_CLOEXEC'):  # On Linux only.
        flags = fcntl.fcntl(fd, fcntl.F_GETFD)
        if inheritable:
            flags &= ~fcntl.FD_CLOEXEC
        else:
            flags |= os.O_CLOEXEC
        fcntl.fcntl(fd, fcntl.F_SETFD, flags)


class InteractorError(Exception):
    def __init__(self, message, interactor_out, env, renv, irenv):
        super().__init__(
            '%s\n'
            'Interactor out: %s\n'
            'Interactor environ dump: %s\n'
            'Solution environ dump: %s\n'
            'Environ dump: %s'
            % (message, interactor_out, irenv, renv, env)
        )


class Pipes:
    """
    Class for storing file descriptors for interactor and solution processes.
    """
    r_interactor = None
    w_interactor = None
    r_solution = None
    w_solution = None

    def __init__(self, r_interactor, w_interactor, r_solution, w_solution):
        """
        Constructor for Pipes class.
        :param r_interactor: file descriptor from which the interactor reads from the solution
        :param w_interactor: file descriptor to which the interactor writes to the solution
        :param r_solution: file descriptor from which the solution reads from the interactor
        :param w_solution: file descriptor to which the solution writes to the interactor
        """
        self.r_interactor = r_interactor
        self.w_interactor = w_interactor
        self.r_solution = r_solution
        self.w_solution = w_solution


def _limit_length(s):
    if len(s) > RESULT_STRING_LENGTH_LIMIT:
        suffix = b'[...]'
        return s[: max(0, RESULT_STRING_LENGTH_LIMIT - len(suffix))] + suffix
    return s


def run(environ, executor, use_sandboxes=True):
    """
    Common code for executors.

    :param: environ Recipe to pass to `filetracker` and `sio.workers.executors`
                    For all supported options, see the global documentation for
                    `sio.workers.executors` and prefix them with ``exec_``.
    :param: executor Executor instance used for executing commands.
    :param: use_sandboxes Enables safe checking output correctness.
                       See `sio.executors.checkers`. True by default.
    """

    if feedback.judge_prepare(environ).force_not_judge:
        environ['time_used'] = 0
        environ['result_string'] = 'not judged'
        environ['result_code'] = 'NJ'
        environ['mem_used'] = 0
        environ['num_syscalls'] = 0
        environ['stderr'] = ''
        return environ

    print('POST judge_prepare')

    renv = _run(environ, executor, use_sandboxes)

    print('POST _run')

    _populate_environ(renv, environ)

    print('POST _populate_environ')

    for key in ('result_code', 'result_string'):
        environ[key] = replace_invalid_UTF(environ[key])
    feedback.judge_finished(environ)

    print('POST judge_finished')

    if 'out_file' in environ:
        ft.upload(
            environ,
            'out_file',
            tempcwd('out'),
            to_remote_store=environ.get('upload_out', False),
        )

    print('POST upload')

    return environ


def _fill_result(env, renv, irenv, interactor_out):
    sol_sig = renv.get('exit_signal', None)
    inter_sig = irenv.get('exit_signal', None)
    sigpipe = signal.SIGPIPE.value

    if six.ensure_binary(interactor_out[0]) != b'':
        renv['result_string'] = ''
        if six.ensure_binary(interactor_out[0]) == b'OK':
            renv['result_code'] = 'OK'
            if interactor_out[1]:
                renv['result_string'] = _limit_length(interactor_out[1])
            renv['result_percentage'] = float(interactor_out[2] or 100)
        else:
            renv['result_code'] = 'WA'
            if interactor_out[1]:
                renv['result_string'] = _limit_length(interactor_out[1])
            renv['result_percentage'] = 0
    elif irenv['result_code'] != 'OK' and irenv['result_code'] != 'TLE' and inter_sig != sigpipe:
        renv['result_code'] = 'SE'
        raise InteractorError('Interactor got %s.' % irenv['result_code'], interactor_out, env, renv, irenv)
    elif renv['result_code'] != 'OK' and sol_sig != sigpipe:
        return
    elif inter_sig == sigpipe:
        renv['result_code'] = 'WA'
        renv['result_string'] = 'solution exited prematurely'
    elif irenv.get('real_time_killed', False):
        renv['result_code'] = 'TLE'
        renv['result_string'] = 'interactor time limit exceeded (user\'s solution or interactor can be the cause)'
    else:
        raise InteractorError('Unexpected interactor error', interactor_out, env, renv, irenv)


def _run(environ, executor, use_sandboxes):
    input_name = tempcwd('in')

    num_processes = environ.get('num_processes', 1)
    file_executor = get_file_runner(executor, environ)
    interactor_executor = DetailedUnprotectedExecutor()
    exe_filename = file_executor.preferred_filename()
    interactor_filename = 'soc'

    ft.download(environ, 'exe_file', exe_filename, add_to_cache=True)
    os.chmod(tempcwd(exe_filename), 0700)
    ft.download(environ, 'interactor_file', interactor_filename, add_to_cache=True)
    os.chmod(tempcwd(interactor_filename), 0700)
    ft.download(environ, 'in_file', input_name, add_to_cache=True)

    zipdir = tempcwd('in_dir')
    os.mkdir(zipdir)
    try:
        input_name = _extract_input_if_zipfile(input_name, zipdir)
        proc_pipes = []

        for i in range(num_processes):
            r1, w1 = os.pipe()
            r2, w2 = os.pipe()
            for fd in (r1, w1, r2, w2):
                set_inheritable(fd, True)
            proc_pipes.append(Pipes(r1, w2, r2, w1))

        print('POST pipework')

        interactor_args = [str(num_processes)]
        for pipes in proc_pipes:
            interactor_args.extend([str(pipes.r_interactor), str(pipes.w_interactor)])

        interactor_time_limit = 2 * environ['exec_time_limit']

        class ExecutionWrapper(Thread):
            def __init__(self, executor, *args, **kwargs):
                super(ExecutionWrapper, self).__init__()
                self.idxd = random.randint(0,9999)
                self.executor = executor
                self.args = args
                self.kwargs = kwargs
                self.value = None
                self.exception = None
            
            def run(self):
                with TemporaryCwd():
                    print('PRE exec', self.idxd, self.kwargs['environ_prefix'])
                    try:
                        self.value = self.executor(*self.args, **self.kwargs)
                    except Exception as e:
                        traceback.print_exc()
                        self.exception = e
                    print('POST exec', self.idxd, self.kwargs['environ_prefix'])

        with open(input_name, 'rb') as infile, open(tempcwd('out'), 'wb') as outfile:
            feedback.judge_started(environ)
            processes = []
            interactor_fds = []
            for pipes in proc_pipes:
                interactor_fds.extend([pipes.r_interactor, pipes.w_interactor])

            with interactor_executor as ie:
                interactor = ExecutionWrapper(
                    ie,
                    [tempcwd(interactor_filename)] + interactor_args,
                    stdin=infile,
                    stdout=outfile,
                    ignore_errors=True,
                    environ=environ,
                    environ_prefix='interactor_',
                    mem_limit=DEFAULT_INTERACTOR_MEM_LIMIT,
                    time_limit=interactor_time_limit,
                    #fds_to_close=interactor_fds,
                    pass_fds=interactor_fds,
                    cwd=tempcwd(),
                )

            for i in range(num_processes):
                pipes = proc_pipes[i]
                with file_executor as fe:
                    exe = ExecutionWrapper(
                        fe,
                        tempcwd(exe_filename),
                        [str(i)],
                        stdin=pipes.r_solution,
                        stdout=pipes.w_solution,
                        ignore_errors=True,
                        environ=environ,
                        environ_prefix='exec_',
                        #fds_to_close=[pipes.r_solution, pipes.w_solution],
                        cwd=tempcwd(),
                    )
                    processes.append(exe)

            for process in processes:
                process.start()
            interactor.start()

            print('POST spawn')

            for process in processes:
                process.join()
            interactor.join()

            print('POST join')

            for pipe in pipes:
                try:
                    os.close(pipe.r_interactor)
                except:
                    pass
                try:
                    os.close(pipe.w_interactor)
                except:
                    pass
                try:
                    os.close(pipe.r_solution)
                except:
                    pass
                try:
                    os.close(pipe.w_solution)
                except:
                    pass

            print('POST close')

            if interactor.exception:
                raise interactor.exception
            for process in processes:
                if process.exception:
                    raise process.exception

            renv = processes[0].value
            for process in processes:
                if process.value['result_code'] != 'OK':
                    renv = process.value
                    break
                renv['time_used'] = max(renv['time_used'], process.value['time_used'])
                renv['mem_used'] = max(renv.get('mem_used', 0), process.value.get('mem_used', 0))

            irenv = interactor.value

            print('POST aggregate')

        try:
            with open(tempcwd('out'), 'rb') as result_file:
                interactor_out = [line.rstrip() for line in result_file.readlines()]
            while len(interactor_out) < 3:
                interactor_out.append(b'')
        except FileNotFoundError:
            interactor_out = []

        print('POST receive')

        _fill_result(environ, renv, irenv, interactor_out)
    finally:
        rmtree(zipdir)

    return renv
