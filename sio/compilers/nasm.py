from sio.compilers.common import Compiler
from sio.workers.util import tempcwd

class NasmCompiler(Compiler):
    sandbox = 'nasm.2_16_01'
    lang = 'nasm'
    output_file = 'a.out'

    def _make_cmdline(self, executor):
        return [
                '/entrypoint',
                tempcwd(self.source_file),
                tempcwd('a.o'),
                tempcwd(self.output_file),
        ]

def run(environ):
    return NasmCompiler().compile(environ)

