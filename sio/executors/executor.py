from __future__ import absolute_import
from sio.executors import common
from sio.workers.executors import YrdenExecutor


def run(environ):
    return common.run(environ, YrdenExecutor('empty-exe'))
