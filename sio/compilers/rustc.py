from __future__ import absolute_import
from sio.compilers.system_rustc import RustCompiler


class RustBoxedCompiler(RustCompiler):
    @classmethod
    def rustc_1_63_0(cls):
        obj = cls('rustc.1_63_0')
        obj.compiler = '/rustc-wrapper'
        return obj


def run_rustc1_63_0(environ):
    return RustBoxedCompiler.rustc_1_63_0().compile(environ)


run_rust_rustc1_63_0 = run_rustc1_63_0
