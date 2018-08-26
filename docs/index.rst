===================================================
Plette: Structured Pipfile and Pipfile.lock models.
===================================================

Plette is an implementation to the Pipfile_ specification. It offers parsers
and style-preserving emitters to both the Pipfile and Pipfile.lock formats,
with optional validators to both files.

.. _Pipfile: https://github.com/pypa/pipfile


Quickstart
==========

Plette is available on PyPI. You can install it with pip:

.. code-block:: none

    pip install plette

Now you can load a Pipfile from path like this::

    >>> import plette
    >>> with open('./Pipfile', encoding='utf-8') as f:
    ...     pipfile = plette.Pipfile.load(f)
    ...

And access contents inside the file::

    >>> pipfile['scripts']['tests']
    'pytest -v tests'

Loading from a lock file works similarly::

    >>> with open('./Pipfile.lock', encoding='utf-8') as f:
    ...     lockfile = plette.Lockfile.load(f)
    ...
    >>> lockfile.meta.sources[0].url
    'https://pypi.org/simple'


Contents
========

.. toctree::
   :maxdepth: 2

   files
   sections
   nested
   validation
