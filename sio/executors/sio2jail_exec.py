from sio.executors import common, encdec_common, interactive_common
from sio.workers.executors import Sio2JailExecutor


def run(environ):
    return common.run(environ, Sio2JailExecutor())


def encdec_run(environ):
    return encdec_common.run(environ, Sio2JailExecutor())


def interactive_run(environ):
    return interactive_common.run(environ, Sio2JailExecutor())
