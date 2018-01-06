from sio.executors import common
#from sio.workers.executors import VCPUExecutor
from sio.workers.executors import IsolateExecutor

def run(environ):
    return common.run(environ, IsolateExecutor())
