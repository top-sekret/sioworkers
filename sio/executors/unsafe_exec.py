from sio.executors import common, interactive_common
from sio.workers.executors import DetailedUnprotectedExecutor
#from sio.workers.executors import IsolateExecutor

def run(environ):
    return common.run(environ, DetailedUnprotectedExecutor(),
            use_sandboxes=False)

def interactive_run(environ):
    return interactive_common.run(environ, DetailedUnprotectedExecutor(),
            use_sandboxes=False)
