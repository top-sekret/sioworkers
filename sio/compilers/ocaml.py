from sio.compilers.common import Compiler
from sio.workers.util import tempcwd
from sio.workers.executors import noquote
import os
import time

class OcamlCompiler(Compiler):
    sandbox = 'ocaml'
    lang = 'ml'
    output_file = 'a'

    def _make_cmdline(self, executor):
        return ['bin/sh', '-c', ['ocamlopt', '-verbose', '-ccopt', '-static', '-I', noquote('$HOME/.sio-sandboxes/compiler-ocaml/usr/lib/ocaml/'), '-o', 'a', 'a.ml']]

def run_ocaml(environ):
    return OcamlCompiler().compile(environ)

run_default_ml = run_ocaml

