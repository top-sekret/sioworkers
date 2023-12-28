from __future__ import absolute_import
from sio.workers import ft
from sio.workers.executors import UnprotectedExecutor, \
    DetailedUnprotectedExecutor, VCPUExecutor, Sio2JailExecutor, \
    SupervisedExecutor, PRootExecutor
from sio.workers.util import RegisteredSubclassesBase, mkdir, tempcwd
import tarfile
import os.path
import six

class LanguageModeWrapper(RegisteredSubclassesBase):
    """Language mode wrapper runs compiled file within ``executor``.

       Wrappers produce shell commands suitable to be run inside executors,
       as not all files are directly executable. For example, to run 'exe.py'
       one needs to execute ``python exe.py`` in a shell.
    """

    abstract = True
    #: Set this in subclasses to register handling execution mode
    handled_exec_mode = None
    #: Set this in subclasses to register list of handled executors
    handled_executors = ()

    @classmethod
    def __classinit__(cls):
        this_cls = globals().get('LanguageModeWrapper', cls)
        super(this_cls, cls).__classinit__()
        cls.wrappers = {}

    @classmethod
    def register_subclass(cls, subcls):
        if cls is not subcls:
            cls.wrappers.setdefault(subcls.handled_exec_mode, {}).update(
                {ex: subcls for ex in subcls.handled_executors})

    @classmethod
    def execution_mode_wrapper(cls, executor, environ):
        exec_info = environ['exec_info']
        try:
            runner = cls.wrappers[exec_info['mode']][type(executor)]
        except KeyError:
            raise SystemError(
                "No way of running file of kind %s in executor %s." %
                (exec_info['mode'], executor))

        return runner(executor, environ)

    def __init__(self, executor, environ):
        self.executor = executor
        self.environ = environ

    def __enter__(self):
        self.executor.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.executor.__exit__(exc_type, exc_value, traceback)

    def __call__(self, file, args, **kwargs):
        """Run given ``file`` in underlying executor with arguments ``args``.

           Keyword arguments are passed to the executor.
        """
        raise NotImplementedError

    def preferred_filename(self):
        """Returns filename to which the file should be downloaded."""
        raise NotImplementedError
    
    def _download_extra_execution_files(self, environ, dest):
        tmp_environ = environ.copy()
        for file_name, file_path in six.iteritems(environ.get('extra_execution_files', {})):
            tmp_environ['extra_execution_file'] = file_path
            ft.download(tmp_environ, 'extra_execution_file',
                        dest=os.path.join(dest, file_name),
                        add_to_cache=True)


class NoOp(LanguageModeWrapper):
    """NoOp wrapper doesn't do any wrapping at all."""

    handled_exec_mode = 'executable'
    handled_executors = ()

    def __call__(self, file, args, **kwargs):
        self._download_extra_execution_files(kwargs.get('environ', os.environ.copy()), '.')
        return self.executor([file] + args, **kwargs)

    def preferred_filename(self):
        return self.environ['exec_info'].get('preferred_filename', 'exe')


class Executable(LanguageModeWrapper):
    """Runs directly executable ``exe`` file with ``./exe``."""

    handled_exec_mode = 'executable'
    handled_executors = UnprotectedExecutor, DetailedUnprotectedExecutor, \
        PRootExecutor, VCPUExecutor, Sio2JailExecutor, SupervisedExecutor

    def __call__(self, file, args, **kwargs):
        if os.path.isabs(file):
            cmd = file
        else:
            cmd = './%s' % file
        self._download_extra_execution_files(kwargs.get('environ', os.environ.copy()), '.')
        return self.executor([cmd] + args, **kwargs)

    def preferred_filename(self):
        return 'exe'


class Python3(LanguageModeWrapper):
    """Wraps a Python3 .pyz archive and takes care of running it."""

    handled_exec_mode = 'python3'
    handled_executors = Sio2JailExecutor,

    def __init__(self, executor, environ):
        exec_info = environ['exec_info']
        executor = Sio2JailExecutor('compiler-' + exec_info.get('version', 'python3.4.2-numpy_i386'))

        super(Python3, self).__init__(executor, environ)
        self.exec_info = exec_info

    def __call__(self, file, args, **kwargs):
        python = [self.exec_info.get('python_bin', '/usr/bin/python3')]

        prog_dir = tempcwd('prog')
        inner_dir = '/tmp'
        main_file =  self.exec_info.get('main_file', '__main__.py')
        inner_file = os.path.join(inner_dir, main_file)
        mkdir(prog_dir)

        with tarfile.open(file) as tf:
            tf.extractall(prog_dir)

        kwargs['no_bind_binary'] = True
        kwargs['binds'] = [('/dev/zero', '/dev/urandom', 'ro,dev'),
                           (prog_dir, inner_dir, 'ro')]

        cmd = python + [inner_file]
        alt_exe = self.exec_info.get('alternate_executable', None)
        if alt_exe:
            env = kwargs.get('env')
            if not env:
                env = os.environ.copy()
                env['LC_ALL'] = 'en_US.UTF-8'
                env['LANGUAGE'] = 'en_US.UTF-8'

            env['PYTHONPATH'] = inner_dir
            kwargs['env'] = env

            cmd = [os.path.join(inner_dir, alt_exe)]

        self._download_extra_execution_files(kwargs.get('environ', os.environ.copy()), prog_dir)
        return self.executor(cmd + args, **kwargs)

    def preferred_filename(self):
        return self.exec_info.get('preferred_filename', 'a.tar')


class _BaseJava(LanguageModeWrapper):
    handled_exec_mode = 'java'

    def __init__(self, executor, environ):
        super(_BaseJava, self).__init__(executor, environ)
        self.exec_info = self.environ['exec_info']

    def preferred_filename(self):
        return '%s.jar' % self.exec_info.get('main_class', 'a')


class Java(_BaseJava):
    """Wraps compiled java's ``.jar`` and takes care of memory limiting."""

    handled_exec_mode = 'java'
    handled_executors = UnprotectedExecutor, DetailedUnprotectedExecutor, \
        PRootExecutor

    def __call__(self, file, args, entry_point=None, **kwargs):
        environ = kwargs.get('environ', {})
        environ_prefix = kwargs.get('environ_prefix', 'exec')
        mem_limit = environ.pop(environ_prefix + 'mem_limit',
                                kwargs.get('mem_limit'))
        if mem_limit:
            options = ['-Xmx%dk' % mem_limit, '-Xms%dk' % mem_limit,
                '-Xss%dk' % mem_limit]
            kwargs['mem_limit'] = None
        else:
            options = []

        if not entry_point and self.exec_info.get('main_class'):
            entry_point = self.exec_info['main_class']

        if entry_point:
            cmd = ['java'] + options + ['-classpath', file, entry_point]
        else:
            cmd = ['java'] + options + ['-jar', file]
        self._download_extra_execution_files(kwargs.get('environ', os.environ.copy()), '.')
        return self.executor(cmd + args, **kwargs)


class JavaSIO(_BaseJava):
    handled_exec_mode = 'java'
    handled_executors = SupervisedExecutor,

    def __call__(self, file, args, **kwargs):
        self._download_extra_execution_files(kwargs.get('environ', os.environ.copy()), '.')
        return self.executor([file] + args,
                             java_sandbox='compiler-java.1_8', **kwargs)


def get_file_runner(executor, environ):
    """Finds appropriate wrapper to run ``environ['exe_file']`` in
       given ``executor``.
    """
    environ.setdefault('exec_info', {'mode': 'executable'})
    return LanguageModeWrapper.execution_mode_wrapper(executor, environ)
