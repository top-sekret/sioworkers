from sio.compilers.system_gcc import CStyleCompiler


class CCompiler(CStyleCompiler):
    sandbox = 'gcc.4_8_2'
    lang = 'c'
    options = ['-std=gnu99', '-static', '-O2', '-s', '-lm']

    def __init__(self, cconf):
        if cconf is not None:
            self.sandbox = cconf['compiler']
            self.options = cconf['cflags'].split(' ')
        super(CCompiler, self).__init__()

class CPPCompiler(CStyleCompiler):
    sandbox = 'gcc.4_8_2'
    lang = 'cpp'
    compiler = 'g++'
    options = ['-std=c++11', '-static', '-O2', '-s', '-lm']

    def __init__(self, cconf):
        if cconf is not None:
            self.sandbox = cconf['compiler']
            self.options = cconf['cxxflags'].split(' ')
        super(CPPCompiler, self).__init__()

def run_gcc(environ):
    return CCompiler(environ.get('cconf')).compile(environ)


def run_gplusplus(environ):
    return CPPCompiler(environ.get('cconf')).compile(environ)


run_default_c = run_gcc
run_default_cpp = run_gplusplus
