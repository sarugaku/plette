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
    what you’re doing.


The ``[pipenv]`` Section
========================

The ``[pipenv]`` section holds pipenv runtime behaviour settings. Plette
exposes it through ``pipfile["pipenv"]``, which returns a ``Pipenv`` instance.


``cool-down-period``
--------------------

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
        ‘30d’

``cool_down_period_timedelta``
    Returns the value as a :class:`datetime.timedelta`, or ``None`` if the key
    is absent::

        >>> section.cool_down_period_timedelta
        datetime.timedelta(days=30)

The property is also writable, and validates the new value before storing it::

    >>> section.cool_down_period = "7d"
    >>> section.cool_down_period_timedelta
    datetime.timedelta(days=7)
