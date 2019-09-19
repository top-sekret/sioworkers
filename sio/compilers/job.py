from __future__ import absolute_import
from __future__ import print_function
import sys
import os.path
import logging

try:
    import json

    json.dumps
except (ImportError, AttributeError):
    import simplejson as json

from sio.workers.util import first_entry_point, threadlocal_dir

logger = logging.getLogger(__name__)


def run(environ):
    if 'compiler' not in environ:
        _, extension = os.path.splitext(environ['source_file'])
        environ['compiler'] = 'default-' + extension[1:].lower()

    logger.debug("running compile job %s %s", environ['compiler'], environ.get('task_id', ''))

    compiler = first_entry_point('sio.compilers',
                                 environ['compiler'].split('.')[0])
    environ = compiler(environ)
    assert 'compiler_output' in environ, \
        "Mandatory key 'compiler_output' not returned by job."
    assert 'result_code' in environ, \
        "Mandatory key 'result_code' not returned by job."
    return environ


def main():
    if len(sys.argv) < 3:
        print("""Usage: %s source output [compiler [extra_compilation_args ...]]

   If source or output path starts with '/', then it's considered to
   be filetracker path, if not, relative to the current directory.""" \
              % sys.argv[0].split('/')[-1])
        raise SystemExit(1)

    import logging
    logging.basicConfig(level=logging.DEBUG)

    # Simulate compile.sh from sio1
    environ = {
            'source_file': sys.argv[1],
            'out_file': sys.argv[2],
            'use_filetracker': 'auto',
            'extra_compilation_args': sys.argv[4:]
        }
    if len(sys.argv) > 3:
        compiler = sys.argv[3].lower()
        if '-' not in compiler:
            compiler = 'default-' + compiler
        environ['compiler'] = compiler

    # FIXME: this is an ugly hack to set tempcwd to current cwd
    threadlocal_dir.tmpdir = os.getcwd()

    run(environ)
    print(json.dumps(environ))
