import ast
import os

from setuptools import find_packages, setup


ROOT = os.path.dirname(__file__)

PACKAGE_NAME = 'plette'

VERSION = None

with open(os.path.join(ROOT, 'src', PACKAGE_NAME, '__init__.py')) as f:
    for line in f:
        if line.startswith('__version__ = '):
            VERSION = ast.literal_eval(line[len('__version__ = '):].strip())
            break
if VERSION is None:
    raise EnvironmentError('failed to read version')


setup(
    # These really don't work.
    package_dir={'': 'src'},
    packages=find_packages('src'),

    package_data={
        '': ['LICENSE*', 'README*'],
    },

    # I need this to be dynamic.
    version=VERSION,
)
