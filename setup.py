from __future__ import absolute_import
from sys import version_info
from setuptools import setup, find_packages

PYTHON_VERSION = version_info[0]

python2_specific_requirements = [
    'supervisor>=3.3.1',
    'enum34',
    'poster',
]

python3_specific_requirements = [
    'bsddb3',
]

python23_universal_requirements = [
    'filetracker>=2.1,<3.0',
    'simplejson',
    'Celery>=3.1.15',
    'Twisted>=15.2.1',
    'sortedcontainers',
    'six',
    'pytest',
    'pytest-runner',
    'pytest-timeout',
]

if PYTHON_VERSION == 2:
    final_requirements = python23_universal_requirements + python2_specific_requirements
else:
    final_requirements = python23_universal_requirements + python3_specific_requirements


setup(
    name = "sioworkers",
    version = '1.3',
    author = "SIO2 Project Team",
    author_email = 'sio2@sio2project.mimuw.edu.pl',
    description = "Programming contest judging infrastructure",
    url = 'https://github.com/sio2project/sioworkers',
    license = 'GPL',

    # we need twisted.plugins in packages to install the sio twisted command
    packages = find_packages() + ['twisted.plugins'],
    namespace_packages = ['sio', 'sio.compilers', 'sio.executors'],

    install_requires=final_requirements,

#    setup_requires = [
#        'pytest-runner',
#    ],

    tests_require = [
        'pytest',
        'pytest-timeout'
    ],

    entry_points = {
        'sio.jobs': [
            'ping = sio.workers.ping:run',
            'compile = sio.compilers.job:run',
            'exec = sio.executors.executor:run',
            'encdec-exec = sio.executors.executor:encdec_run',
            'interactive-exec = sio.executors.executor:interactive_run',
            'sio2jail-exec = sio.executors.sio2jail_exec:run',
            'sio2jail-encdec-exec = sio.executors.sio2jail_exec:encdec_run',
            'sio2jail-interactive-exec = sio.executors.sio2jail_exec:interactive_run',
            'vcpu-exec = sio.executors.vcpu_exec:run',
            'cpu-exec = sio.executors.executor:run',
            'cpu-encdec-exec = sio.executors.executor:encdec_run',
            'cpu-interactive-exec = sio.executors.executor:interactive_run',
            'unsafe-exec = sio.executors.unsafe_exec:run',
            'unsafe-encdec-exec = sio.executors.unsafe_exec:encdec_run',
            'unsafe-interactive-exec = sio.executors.unsafe_exec:interactive_run',
            'ingen = sio.executors.ingen:run',
            'inwer = sio.executors.inwer:run',
        ],
        'sio.compilers': [
            # Example compiler:
            'foo = sio.compilers.template:run',

            # Default extension compilers:
            'default-c = sio.compilers.gcc:run_c_default',
            'default-cc = sio.compilers.gcc:run_cpp_default',
            'default-cpp = sio.compilers.gcc:run_cpp_default',
            'default-pas = sio.compilers.fpc:run_pas_default',
            'default-java = sio.compilers.java:run_java_default',
            'default-py = sio.compilers.python:run_python_default',

            # Sandboxed compilers:
            'c = sio.compilers.gcc:run_c_default',
            'gcc4_8_2_c99 = sio.compilers.gcc:run_c_gcc4_8_2_c99',
            'gcc12_2_0_c17 = sio.compilers.gcc:run_c_gcc12_2_0_c17',

            'cc = sio.compilers.gcc:run_cpp_default',
            'cpp = sio.compilers.gcc:run_cpp_default',
            'g++4_8_2_cpp11 = sio.compilers.gcc:run_cpp_gcc4_8_2_cpp11',
            'g++6_3_cpp14 = sio.compilers.gcc:run_cpp_gcc6_3_cpp14',
            'g++8_3_cpp17 = sio.compilers.gcc:run_cpp_gcc8_3_cpp17',
            'g++8_3_cpp17_amd64 = sio.compilers.gcc:run_cpp_gcc8_3_cpp17_amd64',
            'g++10_2_cpp17_amd64 = sio.compilers.gcc:run_cpp_gcc10_2_cpp17_amd64',
            'g++12_2_cpp20_amd64 = sio.compilers.gcc:run_cpp_gcc12_2_cpp20_amd64',

            'pas = sio.compilers.fpc:run_pas_default',
            'fpc2_6_2 = sio.compilers.fpc:run_pas_fpc2_6_2',

            'java = sio.compilers.java:run_java_default',
            'java1_8 = sio.compilers.java:run_java1_8',

            'python_3_4_numpy = sio.compilers.python:run_python3_4_numpy',
            'python_3_7 = sio.compilers.python:run_python3_7',
            'python_3_7_numpy = sio.compilers.python:run_python3_7_numpy',
            'python_3_7_numpy_amd64 = sio.compilers.python:run_python3_7_numpy_amd64',
            'python_3_9_numpy = sio.compilers.python:run_python3_9_numpy_amd64',
            'python_3_9_numpy_amd64 = sio.compilers.python:run_python3_9_numpy_amd64',
            'python_3_11_numpy_amd64 = sio.compilers.python:run_python3_11_numpy_amd64',
            'py = sio.compilers.python:run_python_default',

            # Compiler for output only tasks solutions
            'output-only = sio.compilers.output:run',

            # Non-sandboxed compilers
            'system-c = sio.compilers.system_gcc:run_gcc',
            'system-gcc = sio.compilers.system_gcc:run_gcc',

            'system-cc = sio.compilers.system_gcc:run_gplusplus',
            'system-cpp = sio.compilers.system_gcc:run_gplusplus',
            'system-g++ = sio.compilers.system_gcc:run_gplusplus',

            'system-pas = sio.compilers.system_fpc:run',
            'system-fpc = sio.compilers.system_fpc:run',

            'system-java = sio.compilers.system_java:run',
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
