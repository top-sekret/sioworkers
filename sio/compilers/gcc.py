from __future__ import absolute_import
from sio.compilers.system_gcc import CStyleCompiler


class CCompiler(CStyleCompiler):
    lang = 'c'

    @classmethod
    def gcc_10_2_1_c17(cls):
        obj = cls('gcc.10_2_1')
        obj.options = ['-std=c17', '-static', '-O3', '-lm']
        return obj


class CPPCompiler(CStyleCompiler):
    lang = 'cpp'

    @classmethod
    def gcc_10_2_1_cpp17(cls):
        obj = cls('gcc.10_2_1')
        obj.compiler = 'g++'
        obj.options = ['-std=c++17', '-static', '-O3']
        return obj


def run_gcc10_2_1_c17(environ):
    return CCompiler.gcc_10_2_1_c17().compile(environ)


def run_gplusplus10_2_1_cpp17(environ):
    return CPPCompiler.gcc_10_2_1_cpp17().compile(environ)


run_c_gcc10_2_1_c17 = run_gcc10_2_1_c17
run_cpp_gcc10_2_1_cpp17 = run_gplusplus10_2_1_cpp17
