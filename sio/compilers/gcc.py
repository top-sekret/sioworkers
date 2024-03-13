from __future__ import absolute_import
from sio.compilers.system_gcc import CStyleCompiler


class CCompiler(CStyleCompiler):
    lang = 'c'

    @classmethod
    def gcc_12_2_0_c17(cls):
        obj = cls('gcc.12_2_0')
        obj.options = ['-std=c17', '-static', '-O3', '-lm']
        return obj


class CPPCompiler(CStyleCompiler):
    lang = 'cpp'

    @classmethod
    def gcc_12_2_0_cpp20(cls):
        obj = cls('gcc.12_2_0')
        obj.compiler = 'g++'
        obj.options = ['-std=c++20', '-static', '-O3']
        return obj


def run_gcc12_2_0_c17(environ):
    return CCompiler.gcc_12_2_0_c17().compile(environ)


def run_gplusplus12_2_0_cpp20(environ):
    return CPPCompiler.gcc_12_2_0_cpp20().compile(environ)


run_c_gcc12_2_0_c17 = run_gcc12_2_0_c17
run_cpp_gcc12_2_0_cpp20 = run_gplusplus12_2_0_cpp20
