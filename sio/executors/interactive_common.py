import os
from shutil import rmtree
from threading import Thread

from sio.executors.checker import output_to_fraction
from sio.executors.common import _extract_input_if_zipfile, _populate_environ
from sio.workers import ft
from sio.workers.executors import DetailedUnprotectedExecutor
from sio.workers.util import TemporaryCwd, decode_fields, replace_invalid_UTF, tempcwd
from sio.workers.file_runners import get_file_runner

import signal
import six

DEFAULT_INTERACTOR_MEM_LIMIT = 256 * 2 ** 10  # in KiB
RESULT_STRING_LENGTH_LIMIT = 1024  # in bytes


class InteractorError(Exception):
    def __init__(self, message, interactor_out, env, renv, irenv):
        super().__init__(
            f'{message}\n'
            f'Interactor out: {interactor_out}\n'
            f'Interactor environ dump: {irenv}\n'
            f'Solution environ dump: {renv}\n'
            f'Environ dump: {env}'
        )


class Pipes:
    r_interactor = None
    w_interactor = None
    r_solution = None
    w_solution = None

    def __init__(self, r_interactor, w_interactor, r_solution, w_solution):
        self.r_interactor = r_interactor
        self.w_interactor = w_interactor
        self.r_solution = r_solution
        self.w_solution = w_solution


def _limit_length(s):
    if len(s) > RESULT_STRING_LENGTH_LIMIT:
        suffix = b'[...]'
        return s[: max(0, RESULT_STRING_LENGTH_LIMIT - len(suffix))] + suffix
    return s


@decode_fields(['result_string'])
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

    renv = _run(environ, executor, use_sandboxes)

    _populate_environ(renv, environ)

    for key in ('result_code', 'result_string'):
        environ[key] = replace_invalid_UTF(environ[key])

    if 'out_file' in environ:
        ft.upload(
            environ,
            'out_file',
            tempcwd('out'),
            to_remote_store=environ.get('upload_out', False),
        )

    return environ


def _fill_result(env, renv, irenv, interactor_out):
    sol_sig = renv.get('exit_signal', None)
    inter_sig = irenv.get('exit_signal', None)
    sigpipe = signal.SIGPIPE.value

    if irenv['result_code'] != 'OK' and inter_sig != sigpipe:
        renv['result_code'] = 'SE'
        raise InteractorError(f'Interactor got {irenv["result_code"]}.', interactor_out, env, renv, irenv)
    elif renv['result_code'] != 'OK' and sol_sig != sigpipe:
        return
    elif len(interactor_out) == 0:
        renv['result_code'] = 'SE'
        raise InteractorError(f'Empty interactor out.', interactor_out, env, renv, irenv)
    elif inter_sig == sigpipe:
        renv['result_code'] = 'WA'
        renv['result_string'] = 'solution exited prematurely'
    else:
        renv['result_string'] = ''
        if six.ensure_binary(interactor_out[0]) == b'OK':
            renv['result_code'] = 'OK'
            if interactor_out[1]:
                renv['result_string'] = _limit_length(interactor_out[1])
            renv['result_percentage'] = output_to_fraction(interactor_out[2])
        else:
            renv['result_code'] = 'WA'
            if interactor_out[1]:
                renv['result_string'] = _limit_length(interactor_out[1])
            renv['result_percentage'] = (0, 1)


def _run(environ, executor, use_sandboxes):
    input_name = tempcwd('in')

    num_processes = environ.get('num_processes', 1)

    file_executor = get_file_runner(executor, environ)
    interactor_executor = DetailedUnprotectedExecutor()
    exe_filename = file_executor.preferred_filename()
    interactor_filename = 'soc'

    ft.download(environ, 'exe_file', exe_filename, add_to_cache=True)
    os.chmod(tempcwd(exe_filename), 0o700)
    ft.download(environ, 'interactor_file', interactor_filename, add_to_cache=True)
    os.chmod(tempcwd(interactor_filename), 0o700)
    ft.download(environ, 'in_file', input_name, add_to_cache=True)

    zipdir = tempcwd('in_dir')
    os.mkdir(zipdir)
    try:
        input_name = _extract_input_if_zipfile(input_name, zipdir)
        pipes = []

        for i in range(num_processes):
            r1, w1 = os.pipe()
            r2, w2 = os.pipe()
            for fd in (r1, w1, r2, w2):
                os.set_inheritable(fd, True)
            pipes.append(Pipes(r1, w1, r2, w2))

        interactor_args = [str(num_processes)]
        # interactor_args = [os.path.basename(input_name), 'out', num_processes]
        for i in range(num_processes):
            interactor_args.append(f'{pipes[i].r_interactor} {pipes[i].w_interactor}')

        interactor_time_limit = 2 * environ['exec_time_limit']

        class ExecutionWrapper(Thread):
            def __init__(self, executor, *args, **kwargs):
                super(ExecutionWrapper, self).__init__()
                self.executor = executor
                self.args = args
                self.kwargs = kwargs
                self.value = None
                self.exception = None

            def run(self):
                with TemporaryCwd():
                    try:
                        self.value = self.executor(*self.args, **self.kwargs)
                    except Exception as e:
                        self.exception = e
        with open(input_name, 'rb') as infile, open(tempcwd('out'), 'wb') as outfile:
            processes = []
            fds_to_close = []
            for pipe in pipes:
                fds_to_close.extend([pipe.r_interactor, pipe.w_interactor, pipe.r_solution, pipe.w_solution])
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
                    fds_to_close=fds_to_close,
                    cwd=tempcwd(),
                )

            for i in range(num_processes):
                with file_executor as fe:
                    exe = ExecutionWrapper(
                        fe,
                        tempcwd(exe_filename),
                        [str(i)],
                        stdin=r1,
                        stdout=w2,
                        ignore_errors=True,
                        environ=environ,
                        environ_prefix='exec_',
                        fds_to_close=fds_to_close,
                        cwd=tempcwd(),
                    )
                    processes.append(exe)

            for process in processes:
                process.start()
            interactor.start()

            for process in processes:
                process.join()
            interactor.join()

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
                renv['mem_used'] = max(renv['mem_used'], process.value['mem_used'])

            irenv = interactor.value

        try:
            with open(tempcwd('out'), 'rb') as result_file:
                interactor_out = [line.rstrip() for line in result_file.readlines()]
            while len(interactor_out) < 3:
                interactor_out.append(b'')
        except FileNotFoundError:
            interactor_out = []

        _fill_result(environ, renv, irenv, interactor_out)
    finally:
        rmtree(zipdir)

    return renv
