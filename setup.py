from setuptools import setup, find_packages

setup(
    name = "sioworkers",
    version = '1.4.4',
    author = "SIO2 Project Team",
    author_email = 'sio2@sio2project.mimuw.edu.pl',
    description = "Programming contest judging infrastructure",
    url = 'https://github.com/sio2project/sioworkers',
    license = 'GPL',

    # we need twisted.plugins in packages to install the sio twisted command
    packages = find_packages() + ['twisted.plugins'],
    namespace_packages = ['sio', 'sio.compilers', 'sio.executors'],

    install_requires = [
        'filetracker>=2.1.5,<3.0',
        'bsddb3==6.2.7',
        'simplejson==3.14.0',
        'supervisor>=4.0,<4.3',
        'Twisted==20.3.0',
        'sortedcontainers==2.1.0',
        'six',
        'urllib3>=1.26.14,<2.0',
    ],

    extras_require = {
        'dev' : [
            'pytest>=7.2.1,<8.0',
            'pytest-timeout==2.1.0',
            'tox',
        ]
    },

    entry_points = {
        'sio.jobs': [
            'ping = sio.workers.ping:run',
            'compile = sio.compilers.job:run',
            'exec = sio.executors.executor:run',
            'sio2jail-exec = sio.executors.sio2jail_exec:run',
            'cpu-exec = sio.executors.executor:run',
            'unsafe-exec = sio.executors.unsafe_exec:run',
            'ingen = sio.executors.ingen:run',
            'inwer = sio.executors.inwer:run',
        ],
        'sio.compilers': [
            # Example compiler:
            'foo = sio.compilers.template:run',

            # Sandboxed compilers:
            'gcc10_2_1_c17 = sio.compilers.gcc:run_c_gcc10_2_1_c17',
            'g++10_2_1_cpp17 = sio.compilers.gcc:run_cpp_gcc10_2_1_cpp17',
            'rustc1_63_0 = sio.compilers.rustc:run_rust_rustc1_63_0',

            # Non-sandboxed compilers
            'system-gcc = sio.compilers.system_gcc:run_gcc',
            'system-g++ = sio.compilers.system_gcc:run_gplusplus',
            'system-fpc = sio.compilers.system_fpc:run',
            'system-java = sio.compilers.system_java:run',
            'system-rustc = sio.compilers.system_rustc:run',

            # Compiler for output only tasks solutions
            'output-only = sio.compilers.output:run',

            'default-c = sio.compilers.gcc:run_c_gcc10_2_1_c17',
            'default-cpp = sio.compilers.gcc:run_cpp_gcc10_2_1_cpp17',
            'default-fpc = sio.compilers.system_fpc:run',
            'default-java = sio.compilers.system_java:run',
            'default-rust = sio.compilers.rustc:run_rust_rustc1_63_0',

            ####################################
            # Deprecated, should be removed after 01.01.2021
            # Non-sandboxed compilers
            'system-c = sio.compilers.system_gcc:run_gcc',

            'system-cc = sio.compilers.system_gcc:run_gplusplus',
            'system-cpp = sio.compilers.system_gcc:run_gplusplus',

            'system-pas = sio.compilers.system_fpc:run',

            'system-rs = sio.compilers.system_rustc:run',
            ####################################
        ],
        'console_scripts': [
            'sio-batch = sio.workers.runner:main',
            'sio-run-filetracker = sio.workers.ft:launch_filetracker_server',
            'sio-get-sandbox = sio.workers.sandbox:main',
            'sio-compile = sio.compilers.job:main',
            'sio-celery-worker = sio.celery.worker:main',
        ]
    }
)


# Make Twisted regenerate the dropin.cache, if possible.  This is necessary
# because in a site-wide install, dropin.cache cannot be rewritten by
# normal users.
try:
    from twisted.plugin import IPlugin, getPlugins
except ImportError:
    pass
# HACK: workaround for hudson
except TypeError:
    pass
else:
    list(getPlugins(IPlugin))
