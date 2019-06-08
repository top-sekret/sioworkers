from sio.compilers.common import Compiler
from sio.workers.util import tempcwd
from sio.workers.executors import noquote
import os
import time

class HaskellCompiler(Compiler):
    sandbox = 'haskell.8_0_1'
    lang = 'hs'
    options = ['-O2', '-optl-O3', '-optl-static', '-optl-pthread']
    output_file = 'a'

    def _make_cmdline(self, executor):
        return ['ghc', 'a.hs'] + self.options + list(self.extra_compilation_args)

def run_haskell(environ):
    return HaskellCompiler().compile(environ)

run_default_hs = run_haskell

