# pylint: disable=attribute-defined-outside-init
from __future__ import absolute_import
import os.path
import glob
import logging
import six
import shutil
import tarfile

from sio.compilers.common import Compiler
from sio.workers.util import tempcwd

logger = logging.getLogger(__name__)

class PythonCompiler(Compiler):
    lang = 'py'
    output_file = 'a.tar'
    python_executable_path = None

    def _make_filename(self):
        source_base = os.path.basename(self.environ['source_file'])
        self.module_name = 'sol' + self.environ.get('problem_short_name',
                                            os.path.splitext(source_base)[0])
        return 'a/%s.py' % self.module_name

    def _process_swig(self, executor, basename):
        swig_in = basename + '.i'
        swig_cxx = basename + '_wrap.cxx'
        swig_o = basename + '_wrap.o'
        lib_cxx = basename + '.cpp'
        lib_o = basename + '.o'
        res_py = basename + '.py'
        res_so = '_%s.so' % basename

        cxxflags = ['-std=c++11', '-O3', '-fPIC']
        includeflag = ['-I/usr/include/python3.4']

        swig = '/usr/bin/swig4.0'
        gxx = '/usr/bin/g++'

        stdout = ''

        swigcmd = [swig, '-c++', '-python', swig_in]
        renv = self._execute(executor, swigcmd)
        stdout += renv['stdout'].decode('utf-8')
        renv['stdout'] = stdout
        if renv['return_code']:
            return renv

        compile_lib = [gxx] + cxxflags + ['-c', lib_cxx]
        renv = self._execute(executor, compile_lib)
        stdout += renv['stdout'].decode('utf-8')
        renv['stdout'] = stdout
        if renv['return_code']:
            return renv

        compile_swig = [gxx] + cxxflags + includeflag + ['-c', swig_cxx]
        renv = self._execute(executor, compile_swig)
        stdout += renv['stdout'].decode('utf-8')
        renv['stdout'] = stdout
        if renv['return_code']:
            return renv

        link = [gxx, '-shared', lib_o, swig_o, '-o', res_so]
        renv = self._execute(executor, link)
        stdout += renv['stdout'].decode('utf-8')
        renv['stdout'] = stdout
        if renv['return_code']:
            return renv

        shutil.move(tempcwd(res_so), tempcwd(self._source_dir))
        shutil.move(tempcwd(res_py), tempcwd(self._source_dir))

        return renv

    def _process_wrapper(self, executor, wrapper):
        source_base = os.path.basename(self.source_file)
        cxxflags = ['-std=c++11', '-O3', '-fPIC', '-DSOL_NAME=\"%s\"' % self.module_name, '-I/usr/include/python3.4m']

        gxx = '/usr/bin/g++'

        cxx_files = []
        o_files = []
        res_exe = ''
        with open(tempcwd(wrapper)) as f:
            cxx_files = f.readline().strip('\n').split()
            o_files = f.readline().strip('\n').split()
            res_exe = f.readline().strip('\n')

        stdout = ''
        for cxx_file in cxx_files:
            compile_lib = [gxx] + cxxflags + ['-c', cxx_file]
            renv = self._execute(executor, compile_lib)
            stdout += renv['stdout']
            renv['stdout'] = stdout
            if renv['return_code']:
                return renv

        link = [gxx, '-lpython3.4m', '-o', res_exe] + o_files
        renv = self._execute(executor, link)
        stdout += renv['stdout']
        renv['stdout'] = stdout
        if renv['return_code']:
            return renv

        shutil.move(tempcwd(res_exe), tempcwd(self._source_dir))
        self._alt_executable = res_exe

        return renv

    def _run_in_executor(self, executor):
        python = [self.python_executable_path]

        source_dir = os.path.dirname(self.source_file)
        self._source_dir = source_dir
        self._alt_executable = None

        extra_files = self.environ.get('extra_files', {})
        logger.debug('extra_files: %r', extra_files)
        for extra_file in six.iterkeys(extra_files):
            if extra_file.endswith('.i'):
                logger.debug('swig: %s', extra_file)
                renv = self._process_swig(executor, extra_file[:-2])
            elif extra_file.endswith('.wrapper'):
                logger.debug('wrapper: %s', extra_file)
                renv = self._process_wrapper(executor, extra_file)
            else:
                continue
            if renv['return_code']:
                return renv


        compileall = python + ['-m', 'compileall',
                               self.rcwd(source_dir),
                              ]
        renv = self._execute(executor, compileall)
        if renv['return_code']:
            return renv

        with tarfile.open(tempcwd(self.output_file), 'w:') as tar:
            tar.add(tempcwd(source_dir), '.', True)

        return renv

    def _execute(self, executor, cmdline, **kwargs):
        kwargs.setdefault('mem_limit', None)
        kwargs.setdefault('binds', []).extend([
                    ('/dev/zero', '/dev/urandom', 'ro,dev'),
                ])
        return super(PythonCompiler, self)._execute(executor, cmdline, **kwargs)

    def _postprocess(self, renv):
        environ = super(PythonCompiler, self)._postprocess(renv)
        if environ['result_code'] == 'OK':
            environ['exec_info'] = {
                    'mode': 'python3',
                    'version': self.sandbox,
                    'python_bin': self.python_executable_path,
                    'preferred_filename': 'a.tar',
                    'main_file': '%s.py' % self.module_name,
            }
            if self._alt_executable:
                environ['exec_info']['alternate_executable'] = self._alt_executable
        return environ

    @classmethod
    def python_3_4_numpy(cls):
        obj = cls('python3.4.2-numpy_i386')
        obj.python_executable_path = '/usr/bin/python3.4'
        return obj

    @classmethod
    def python_3_7(cls):
        obj = cls('python3.7_i386')
        obj.python_executable_path = '/usr/bin/python3.7'
        return obj

    @classmethod
    def python_3_7_numpy(cls):
        obj = cls('python3.7.3-numpy_i386')
        obj.python_executable_path = '/usr/bin/python3.7'
        return obj

    @classmethod
    def python_3_7_numpy_amd64(cls):
        obj = cls('python3.7.3-numpy_amd64')
        obj.python_executable_path = '/usr/bin/python3.7'
        return obj

    @classmethod
    def python_3_9_numpy_amd64(cls):
        obj = cls('python3.9.2-numpy_amd64')
        obj.python_executable_path = '/usr/bin/python3.9'
        return obj

    @classmethod
    def python_3_11_numpy_amd64(cls):
        obj = cls('python3.11.2-numpy_amd64')
        obj.python_executable_path = '/usr/bin/python3.11'
        return obj



def run_python3_4_numpy(environ):
    return PythonCompiler().python_3_4_numpy().compile(environ)

def run_python3_7(environ):
    return PythonCompiler().python_3_7().compile(environ)

def run_python3_7_numpy_amd64(environ):
    return PythonCompiler().python_3_7_numpy_amd64().compile(environ)

def run_python3_7_numpy(environ):
    return PythonCompiler().python_3_7_numpy().compile(environ)

def run_python3_9_numpy_amd64(environ):
    return PythonCompiler().python_3_9_numpy_amd64().compile(environ)

def run_python3_11_numpy_amd64(environ):
    return PythonCompiler().python_3_11_numpy_amd64().compile(environ)

run_python_default = run_python3_4_numpy
