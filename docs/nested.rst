==============================
Working with Nested Structures
==============================

It should be enough to work with Plette via the two top-level classes,
``Pipfile`` and ``Lockfile``, in general, and let Plette handle automatic
type conversion for you. Sometimes, however, you would want to peek under the
hood. This chapter discusses how you can handle those structures yourself.

The ``plette.models`` submodule contains definitions of nested structures in
Pipfile and Pipfile.lock, such as indivisual entries in ``[packages]``,
``[dev-packages]``, and ``lockfile['_meta']``.


The Data View
=============

Every non-scalar valuea you get from Plette (e.g. sequence, mapping) is
represented as a `DataView`, or one of its subclasses. This class is simply a
wrapper around the basic collection class, and you can access the underlying
data strucuture via the ``_data`` attribute::

    >>> import plette.models
    >>> source = plette.models.Source({
    ...     'name': 'pypi',
    ...     'url': 'https://pypi.org/simple',
    ...     'verify_ssl': True,
    ... })
    ...
    >>> source._data
    {'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}


Data View Collections
=====================

There are two special collection classes, ``DataViewMapping`` and
``DataViewSequence``, that hold homogeneous ``DataView`` members. They are
also simply wrappers to ``dict`` and ``list``, respectively, but have specially
implemented magic methods to automatically coerce contained data into a
``DataView`` subclass::

    >>> sources = plette.models.SourceCollection([source._data])
    >>> sources._data
    [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}]
    >>> type(sources[0])
    <class 'plette.models.sources.Source'>
    >>> sources[0] == source
    True
    >>> sources[0] = {
    ...     'name': 'devpi',
    ...     'url': 'http://localhost/simple',
    ...     'verify_ssl': True,
    ... }
    ...
    >>> sources._data
    [{'name': 'devpi', 'url': 'http://localhost/simple', 'verify_ssl': True}]
