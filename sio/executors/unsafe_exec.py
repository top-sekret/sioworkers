from sio.executors import common
from sio.workers.executors import DetailedUnprotectedExecutor
#from sio.workers.executors import IsolateExecutor

def run(environ):
    return common.run(environ, DetailedUnprotectedExecutor(),
            use_sandboxes=False)
