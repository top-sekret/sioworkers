from __future__ import absolute_import
from sio.executors import common
from sio.workers.executors import SupervisedExecutor, Sio2JailExecutor

def run(environ):
    return common.run(environ, Sio2JailExecutor(measure_real_time=True))
    #return common.run(environ, SupervisedExecutor())
