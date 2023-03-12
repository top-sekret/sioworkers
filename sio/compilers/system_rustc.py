from __future__ import absolute_import
import os.path

from sio.compilers.common import Compiler
from sio.workers.util import tempcwd


class RustCompiler(Compiler):
    lang = 'rust'
    output_file = 'a.out'
    compiler = 'rustc'
    options = ['-C', 'linker=/usr/bin/rust-clang', '-C', 'lto=thin', '-C', 'opt-level=3', '-C', 'target-feature=+crt-static']

    def _execute(self, cmdline, executor, **kwargs):
        return super(RustCompiler, self)._execute(cmdline, executor, mem_limit=2**26, **kwargs)

    def _make_cmdline(self, executor):
        cmdline = (
            [self.compiler, tempcwd(self.source_file), '-o', tempcwd(self.output_file)]
            + self.options
            + list(self.extra_compilation_args)
        )

        cmdline.extend(
            tempcwd(os.path.basename(source)) for source in self.additional_sources
        )
        return cmdline


def run(environ):
    return RustCompiler().compile(environ)
