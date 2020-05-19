from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.md')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'nepc', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='nepc',
    version=version['__version__'],
    description='Build, access, and explore a NEPC database.',
    long_description=('Build, access, and explore an NRL Evaluated Plasma ' +
                      'Chemistry (NEPC) database.'),
    author='Paul Adamson',
    author_email='paul.adamson@nrl.navy.mil',
    license='',
    packages=['nepc', 'nepc.util'],
    #   no dependencies in this example
    #   install_requires=[
    #       'dependency==1.2.3',
    #   ],
    #   no scripts in this example
    #   scripts=['bin/a-script'],
    include_package_data=True,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    classifiers=[
        'Development Status :: 1 - Development',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7'],
    )
