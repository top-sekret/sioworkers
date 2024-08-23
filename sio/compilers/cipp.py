from sio.compilers.common import Compiler
from sio.workers.util import tempcwd

class CippCompiler(Compiler):
    sandbox = 'cipp.2_1_37'
    lang = 'cipp'
    output_file = 'a.out'

    def _make_cmdline(self, executor):
        return [
                '/entrypoint',
                tempcwd(self.source_file),
                tempcwd('a.temp.cpp'),
                tempcwd(self.output_file),
        ]

def run(environ):
    return CippCompiler().compile(environ)

