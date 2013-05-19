import os
import urllib2
import urlparse
import time
import shutil
import logging

logger = logging.getLogger(__name__)

import filetracker
from sio.workers import _original_cwd, util

_instance = None
def instance():
    """Returns a singleton instance of :class:`filetracker.Client`."""
    global _instance
    if _instance is None:
        launch_filetracker_server()
        _instance = filetracker.Client()
    return _instance

def set_instance(client):
    """Sets the singleton :class:`filetracker.Client` to the given
       object."""
    global _instance
    _instance = client

def _use_filetracker(name, environ):
    mode = environ.get('use_filetracker', True)
    if mode == 'auto':
        return name.startswith('/')
    return bool(mode)

def download(environ, key, dest=None, skip_if_exists=False, **kwargs):
    """Downloads the file from ``environ[key]`` and saves it to ``dest``.

       ``dest``
         A filename, directory name or ``None``. In the two latter cases,
         the file is named the same as in ``environ[key]``.

       ``skip_if_exists``
         If ``True`` and ``dest`` points to an existing file (not a directory
         or ``None``), then the file is not downloaded.

       ``**kwargs``
         Passed directly to :meth:`filetracker.Client.get_file`.

       The value under ``environ['use_filetracker']`` affects downloading
       in the followins way:

       * if ``True``, nothing special happens

       * if ``False``, the file is not downloaded from filetracker, but the
         passed path is assumed to be a regular filesystem path

       * if ``'auto'``, the file is assumed to be a local filename only if
         it is a relative path (this is usually the case when developers play).

       Returns the path to the saved file.
    """

    if dest and skip_if_exists and os.path.exists(dest):
        return dest
    source = environ[key]
    if dest is None:
        dest = os.path.split(source)[1]
    elif dest.endswith(os.sep):
        dest = os.path.join(dest, os.path.split(source)[1])
    if not _use_filetracker(source, environ):
        source = os.path.join(_original_cwd, source)
        if not os.path.exists(dest) or not os.path.samefile(source, dest):
            shutil.copy(source, dest)
    else:
        kwargs.setdefault('add_to_cache', False)
        logger.debug("Downloading %s", source)
        perf_timer = util.PerfTimer()
        instance().get_file(source, dest, **kwargs)
        logger.debug(" completed in %.2fs", perf_timer.elapsed)
    return dest

def upload(environ, key, source, dest=None, **kwargs):
    """Uploads the file from ``source`` to filetracker under ``environ[key]``
       name.

       ``source``
         Filename to upload.

       ``dest``
         A filename, directory name or ``None``. In the two latter cases,
         the file is named the same as in ``environ[key]``.

       ``**kwargs``
         Passed directly to :meth:`filetracker.Client.put_file`.

       See the note about ``environ['use_filetracker']`` in
       :func:`sio.workers.ft.download`.

       Returns the filetracker path to the saved file.
    """

    if dest is None or key in environ:
        dest = environ[key]
    elif dest.endswith(os.sep):
        dest = os.path.join(dest, os.path.split(source)[1])
    if not _use_filetracker(dest, environ):
        dest = os.path.join(_original_cwd, dest)
        if not os.path.exists(dest) or not os.path.samefile(source, dest):
            shutil.copy(source, dest)
    else:
        logger.debug("Uploading %s", dest)
        perf_timer = util.PerfTimer()
        dest = instance().put_file(dest, source, **kwargs)
        logger.debug(" completed in %.2fs", perf_timer.elapsed)
    environ[key] = dest
    return dest

def _do_launch():
    saved_environ = os.environ.copy()
    try:
        # During cleanup Hudson kills all processes with the following
        # environment variables set appropriately. We do not want
        # the filetracker server to be killed, hence we unset those
        # temporarily.
        for var in ('HUDSON_SERVER_COOKIE', 'BUILD_NUMBER', 'BUILD_ID',
                'BUILD_TAG', 'JOB_NAME'):
            del os.environ[var]

        from filetracker.servers.run import main
        main(['-l', '0.0.0.0'])
        time.sleep(5)
    finally:
        os.environ = saved_environ

def launch_filetracker_server():
    """Launches the Filetracker server if ``FILETRACKER_PUBLIC_URL`` is present
       in ``os.environ`` and the server does not appear to be running.

       The server is run in the background and the function returns once the
       server is up and running.
    """

    if 'FILETRACKER_PUBLIC_URL' not in os.environ:
        return
    public_url = os.environ['FILETRACKER_PUBLIC_URL'].split()[0]
    try:
        urllib2.urlopen(public_url + '/status')
        return
    except urllib2.URLError, e:
        logger.info('No Filetracker at %s (%s), launching', public_url, e)
        _do_launch()

if __name__ == '__main__':
    launch_filetracker_server()
