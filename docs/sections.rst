==================
Top-Level Sections
==================

This chapter discusses how you can access and manipulate top-level sections
in a Pipfile and Pipfile.lock through a loaded model.


Sections as Properties
======================

The Pipfile specification defines a set of standard fields a Pipfile may
contain. Those sections are available for access with the dot notation
(property access)::

    >>> for script in pipfile.scripts:
    ...     print(script)
    ...
    build
    changelog
    docs
    draft
    release
    tests

Most property names map directly to the section names defined in the
specification, with dashes replaced by underscored::

    >>> for package in pipfile.dev_packages:
    ...     print(package)
    invoke
    parver
    towncrier
    twine
    wheel
    pytest
    pytest-xdist
    pytest-cov
    sphinx
    sphinx-rtd-theme

For ergonomic concerns, some sections have aliases so they have more Pythonic
names::

    >>> for source in pipfile.sources:
    ...     print(source['url'])
    ...
    https://pypi.org/simple
    >>> for key in lockfile.meta:
    ...     print(key)
    ...
    hash
    pipfile-spec
    requires
    sources

.. tip::

    The canonical names are still available as properties, so you can use
    ``pipfile.source`` and ``lockfile._meta`` if you want to.

The section properties are all writable, so you can use them to manipulate
contents in of the Pipfile (or Pipfile.lock, although not recommended)::

    >>> pipfile.requires = {'python_version': '3.7'}
    >>> pipfile.requires.python_version
    '3.7'


Key-Value Access
================

The Pipfile specification allows arbitrary sections. Those sections are
available with the bracket (key-value) syntax. Standard dict methods such as
``get()`` are also available::

    >>> pipfile.get('pipenv', {}).get('allow_prereleases', False)
    False

.. note::

    The bracket syntax is also available for standard sections. They are only
    available in their canonical forms, however, not in normalized forms or
    aliases, so you will need to use keys like ``pipfile['dev-packages']``,
    ``lockfile['_meta']``, etc.


Missing Sections
================

The Pipfile specification allows any top-level sections to be missing. Plette
does *not* attempt to normalize most them, and will raise `KeyError` or
`AttributeError` if you access a missing key, to distinguish them from blank
sections. You need to catch them manually, or use convenience dict methods
(e.g. ``get()``).

One exception to this rule is the ``source`` section in Pipfile. The
specification explicitly states there will be a default source, and Plette
reflects this by automatically adding one if the loaded Pipfile does not
contain any sources. This means that the ``source`` section will always be
present and not empty when you load it.

The automatically generated source contains the following data

.. code-block:: none

    name = "pypi"
    url = "https://pypi.org/simple"
    verify_ssl = true

.. warning::

    You *can* delete either the automatically generated source, or the source
    section itself from the model after it is loaded. Plette assumes you know
    what you're doing.


Reserved Section Names
======================

Pipfile supports custom package categories beyond the built-in ``[packages]``
and ``[dev-packages]`` sections. Any top-level section that is not a reserved
name is treated as a custom package category and validated accordingly.

The following section names are **reserved** in a Pipfile and cannot be used
as custom package category names:

+------------------+------------------+------------------------------------------+
| Section name     | Model class      | Purpose                                  |
+==================+==================+==========================================+
| ``source``       | ``SourceCollection`` | Package index sources                |
+------------------+------------------+------------------------------------------+
| ``packages``     | ``PackageCollection`` | Default (production) dependencies   |
+------------------+------------------+------------------------------------------+
| ``dev-packages`` | ``PackageCollection`` | Development dependencies            |
+------------------+------------------+------------------------------------------+
| ``requires``     | ``Requires``     | Python version constraints               |
+------------------+------------------+------------------------------------------+
| ``scripts``      | ``ScriptCollection`` | Runnable script shortcuts            |
+------------------+------------------+------------------------------------------+
| ``pipfile``      | ``PipfileSection``   | Pipfile-level metadata               |
+------------------+------------------+------------------------------------------+
| ``pipenv``       | ``Pipenv``       | pipenv runtime behaviour settings        |
+------------------+------------------+------------------------------------------+

Similarly, the following section names are reserved in a **Pipfile.lock** and
cannot be used as custom package category names:

+------------------+------------------+------------------------------------------+
| Section name     | Model class      | Purpose                                  |
+==================+==================+==========================================+
| ``_meta``        | ``Meta``         | Lock file metadata (hash, sources, …)    |
+------------------+------------------+------------------------------------------+
| ``default``      | ``PackageCollection`` | Locked production dependencies      |
+------------------+------------------+------------------------------------------+
| ``develop``      | ``PackageCollection`` | Locked development dependencies     |
+------------------+------------------+------------------------------------------+

All other top-level sections in a Pipfile.lock are treated as custom package
categories and validated as ``PackageCollection`` instances.

.. note::

    Using a reserved name for a custom package category in a Pipfile will
    cause Plette to interpret that section through its reserved model class
    rather than as a package collection. Validation may then fail, or the
    section may be silently misinterpreted. Always choose a name that is not
    in the tables above for custom categories.


Pipfile Sections in Detail
==========================

``[source]``
------------

A list of package index entries. Each entry is validated as a ``Source``
with three required fields:

- ``name`` — a short identifier for the index
- ``url`` — the URL of the "simple" package API; environment variables in the
  form ``$VAR`` or ``${VAR}`` are expanded by the ``url_expanded`` property
- ``verify_ssl`` — whether SSL certificates should be verified (boolean)

::

    >>> source = pipfile.sources[0]
    >>> source.name
    'pypi'
    >>> source.url
    'https://pypi.org/simple'
    >>> source.verify_ssl
    True


``[packages]`` and ``[dev-packages]``
--------------------------------------

Both sections are ``PackageCollection`` mappings whose values are ``Package``
instances. Custom package categories follow the same model. Package values may
be a plain version string or an inline table with additional specifiers::

    >>> pipfile.packages["requests"].version
    '*'


``[requires]``
--------------

Declares the Python version required by the project. Both fields are optional:

- ``python_version`` — a major.minor string, e.g. ``"3.11"``
- ``python_full_version`` — a full version string, e.g. ``"3.11.4"``

::

    >>> pipfile.requires.python_version
    '3.11'


``[scripts]``
-------------

A mapping of short names to shell command strings, used by ``pipenv run``::

    >>> pipfile.scripts["tests"]
    'pytest -v tests'


``[pipfile]``
-------------

Holds Pipfile-level metadata. Currently recognised keys:

- ``sort_pipfile`` (bool) — hint to tooling to keep the Pipfile sorted


``[pipenv]``
------------

Controls pipenv runtime behaviour. Recognised keys:

- ``allow_prereleases`` (bool) — allow pre-release versions when resolving
- ``cool-down-period`` (string, format ``"<int>d"``) — skip re-downloading
  packages fetched within the given number of days (see below)

::

    >>> section = pipfile["pipenv"]
    >>> section["allow_prereleases"]
    True


``cool-down-period``
~~~~~~~~~~~~~~~~~~~~

The ``cool-down-period`` key instructs pipenv to skip re-downloading packages
that were already fetched within the specified window. Its value must follow
the format ``"<int>d"``, where the integer is the number of days:

.. code-block:: toml

    [pipenv]
    cool-down-period = "30d"

Plette validates the format on load and raises ``DataValidationError`` for
invalid values (e.g. ``"30days"``, ``"abc"``, or a non-string).

Two properties are available on the returned ``Pipenv`` instance:

``cool_down_period``
    Returns the raw string value (e.g. ``"30d"``), or ``None`` if the key is
    absent::

        >>> section = pipfile["pipenv"]
        >>> section.cool_down_period
        '30d'

``cool_down_period_timedelta``
    Returns the value as a :class:`datetime.timedelta`, or ``None`` if the key
    is absent::

        >>> section.cool_down_period_timedelta
        datetime.timedelta(days=30)

The property is also writable, and validates the new value before storing it::

    >>> section.cool_down_period = "7d"
    >>> section.cool_down_period_timedelta
    datetime.timedelta(days=7)


Pipfile.lock Sections in Detail
================================

``_meta``
---------

Contains lock file metadata. All four fields are required:

- ``hash`` — SHA-256 hash of the Pipfile used to generate the lock file
- ``pipfile-spec`` — integer version of the Pipfile spec (currently ``6``)
- ``requires`` — Python version constraints copied from the Pipfile
- ``sources`` — list of package index sources copied from the Pipfile

::

    >>> lockfile.meta.pipfile_spec
    6
    >>> lockfile.meta.sources[0].url
    'https://pypi.org/simple'


``default`` and ``develop``
----------------------------

Locked dependency sets for production and development respectively. Both are
``PackageCollection`` mappings. Custom categories in the lock file follow the
same model.
