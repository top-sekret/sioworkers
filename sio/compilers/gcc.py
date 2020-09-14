from __future__ import absolute_import
from sio.compilers.system_gcc import CStyleCompiler


class CCompiler(CStyleCompiler):
    lang = 'c'

    @classmethod
    def gcc_4_8_2_c99(cls):
        obj = cls('gcc.4_8_2')
        obj.options = ['-std=gnu99', '-static', '-O3', '-s', '-lm']
        return obj


class CPPCompiler(CStyleCompiler):
    lang = 'cpp'

    @classmethod
    def gcc_4_8_2_cpp11(cls):
        obj = cls('gcc.4_8_2')
        obj.compiler = 'g++'
        obj.options = ['-std=c++11', '-static', '-O3', '-s']
        return obj

    @classmethod
    def gcc_6_3_cpp14(cls):
        obj = cls('gcc.6_3_0')
        obj.compiler = 'g++'
        obj.options = ['-std=c++14', '-static', '-O3', '-s']
        return obj

    @classmethod
    def gcc_8_3_cpp17(cls):
        obj = cls('gcc.8_3_0-i386')
        obj.compiler = 'g++'
        obj.options = ['-std=c++17', '-static', '-O3', '-s']
        return obj

    @classmethod
    def gcc_8_3_cpp17_amd64(cls):
        obj = cls('gcc.8_3_0-amd64')
        obj.compiler = 'g++'
        obj.options = ['-std=c++17', '-static', '-O3', '-s']
        return obj

def run_gcc4_8_2_c99(environ):
    return CCompiler.gcc_4_8_2_c99().compile(environ)


def run_gcc_default(environ):
    return CCompiler.gcc_4_8_2_c99().compile(environ)


def run_gplusplus4_8_2_cpp11(environ):
    return CPPCompiler.gcc_4_8_2_cpp11().compile(environ)


def run_gplusplus6_3_cpp14(environ):
    return CPPCompiler.gcc_6_3_cpp14().compile(environ)


def run_gplusplus8_3_cpp17(environ):
    return CPPCompiler.gcc_8_3_cpp17().compile(environ)


def run_gplusplus8_3_cpp17_amd64(environ):
    return CPPCompiler.gcc_8_3_cpp17_amd64().compile(environ)


def run_gplusplus_default(environ):
    return CPPCompiler.gcc_4_8_2_cpp11().compile(environ)


run_c_default = run_gcc_default
run_c_gcc4_8_2_c99 = run_gcc4_8_2_c99
run_cpp_default = run_gplusplus_default
run_cpp_gcc4_8_2_cpp11 = run_gplusplus4_8_2_cpp11
run_cpp_gcc6_3_cpp14 = run_gplusplus6_3_cpp14
run_cpp_gcc8_3_cpp17 = run_gplusplus8_3_cpp17
run_cpp_gcc8_3_cpp17_amd64 = run_gplusplus8_3_cpp17_amd64
