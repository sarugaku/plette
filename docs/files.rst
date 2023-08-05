========================
Loading and Saving Files
========================

This chapter discusses how you can load a Pipfile or Pipfile.lock file into a
model, and write it back on the disk.


Loading a File into a Model
===========================

The Pipfile and lock file can be loaded with the customary ``load()`` method.
This method takes a file-like object to load the file::

    >>> import plette
    >>> with open('Pipfile', encoding='utf-8') as f:
    ...     pipfile = plette.Pipfile.load(f)

.. warning::

    This will not work for Python 2, since the loader is very strict about
    file encodings, and only accepts a Unicode file. You are required to use
    ``io.open()`` to open the file instead.

For manipulating a binary file (maybe because you want to interact with a
temporary file created via ``tempfile.TemporaryFile()``), ``load()`` accepts
a second, optional argument::

    >>> import io
    >>> with io.open('Pipfile.lock', 'rb') as f:
    ...     lockfile = plette.Lockfile.load(f, encoding='utf-8')


Writing a File from the Model
=============================

The loaded model can be written to disk with the customary ``dump()`` method.
For a Pipfile, the dumping logic attempts to preserve the original TOML format
as well as possible.

Lock files, on the other hand, are always dumped with the same parameters, to
normalize the JSON output. The lock file’s format matches the reference
implementation, i.e.::

     indent=4,
     separators=(',', ': '),
     sort_keys=True,

``dump()`` always outputs Unicode by default. Similar to ``load()``, it takes
an optional ``encoding`` argument. If set, the output would be in bytes,
encoded with the specified encoding.

Both the Pipfile and Pipfile.lock are guaranteed to be dumped with a trailing
newline at the end.
