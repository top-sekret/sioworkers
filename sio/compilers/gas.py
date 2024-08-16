from sio.compilers.common import Compiler
from sio.workers.util import tempcwd

class GasCompiler(Compiler):
    sandbox = 'gas.2_40'
    lang = 'gas'
    output_file = 'a.out'

    def _make_cmdline(self, executor):
        return [
                '/entrypoint',
                tempcwd(self.source_file),
                tempcwd('a.o'),
                tempcwd(self.output_file),
        ]

def run(environ):
    return GasCompiler().compile(environ)

