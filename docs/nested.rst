==============================
Working with Nested Structures
==============================

It should be enough to work with Plette via the two top-level classes,
``Pipfile`` and ``Lockfile``, in general, and let Plette handle automatic
type conversion for you. Sometimes, however, you would want to peek under the
hood. This chapter discusses how you can handle those structures yourself.

The ``plette.models`` submodule contains definitions of nested structures in
Pipfile and Pipfile.lock, such as individual entries in ``[packages]``,
``[dev-packages]``, and ``lockfile['_meta']``.


Base Model 
===========

Every non-scalar value you get from Plette (e.g. sequence, mapping) is
represented inherits from `models.BaseModel`, which is a Python `dataclass`::

    >>> import plette.models
    >>> source = plette.models.Source(**{
    ...     'name': 'pypi',
    ...     'url': 'https://pypi.org/simple',
    ...     'verify_ssl': True,
    ... })
    ...
    >>> source
    Source(name='pypi', verify_ssl=True, url='https://pypi.org/simple')


Collections
===========

There a few special collection classes, which can be I dentified by the
suffix ``Collection`` or ``Specifiers``.
They group attributes and behave like ``list`` or ``mappings``.
These classes accept a list of dictionaries as input,
and convert them to the correct object type::

    >>> SourceCollection([{'name': 'r-pi', 'url': '192.168.1.129:8000', 'verify_ssl': False}, {'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}])
    SourceCollection(sources=[Source(name='r-pi', verify_ssl=False, url='192.168.1.129:8000'), Source(name='pypi', verify_ssl=True, url='https://pypi.org/simple')])
    

In addition, they can also accept a list of items of the correct type::

    >>> rpi = models.Source(**{'name': 'r-pi', 'url': '192.168.1.129:8000', 'verify_ssl': False})
    >>> pypi = models.Source(**{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True})
    >>> SourceCollection([rpi, pypi])
    SourceCollection(sources=[Source(name='r-pi', verify_ssl=False, url='192.168.1.129:8000'), Source(name='pypi', verify_ssl=True, url='https://pypi.org/simple')])

They can also be indexed by name, and can be iterated over::

    >>> sc = SourceCollection([{'name': 'r-pi', 'url': '192.168.1.129:8000', 'verify_ssl': False}, {'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}])
    >>> sc[0]
    Source(name='r-pi', verify_ssl=False, url='192.168.1.129:8000')
