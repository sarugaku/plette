0.4.2 (2022-10-11)
==================

Bug Fixes
---------

- Add logic to populate the ``default`` and ``develop`` package sections from the ``Pipfile`` to ``with_meta_from``.  `#26 <https://github.com/sarugaku/plette/issues/26>`_
  
- Change validation schema for Requires object to allow for both ``python_version`` and ``python_full_version``.  `#5395 <https://github.com/sarugaku/plette/issues/5395>`_

0.4.1 (2022-10-10)
==================

- Exclude ``pipenv`` section from ``Pipfile`` hash generation as this was a regression caused by named package categories.  `#29 <https://github.com/sarugaku/plette/issues/29>`_
0.4.0 (2022-10-08)
==================

- Add support for named catergories.

0.3.1 (2022-09-21)
==================

- Bug fix.

0.3.0 (2022-09-06)
==================

- Drop Python2 support.

0.2.3 (2019-10-19)
==================

Features
--------

- Show the error details in ``ValidationError``.  `#10 <https://github.com/sarugaku/plette/issues/10>`_
  

Bug Fixes
---------

- Ensure the data to be validated is converted to python dict.  `#8 <https://github.com/sarugaku/plette/issues/8>`_


0.2.2 (2018-08-31)
==================

Bug Fixes
---------

- Fix compatibility to Python < 3.6.


0.2.1 (2018-08-31)
==================

Bug Fixes
---------

- Implement extra conversion logic when copying data from Pipfile to Lockfile models to ensure we get the right things in.  `#5 <https://github.com/sarugaku/plette/issues/5>`_


0.2.0 (2018-08-26)
==================

Features
--------

- Implement `__delitem__` to delete entries from a data view.  `#3 <https://github.com/sarugaku/plette/issues/3>`_

- Add slicing support to `DataViewSequence`. It is not possible to get, set, or
  delete a slice from it. For `__getitem__`, the return value’s type would match
  the sliced `DataViewSequence`.  `#4 <https://github.com/sarugaku/plette/issues/4>`_


0.1.1 (2018-08-19)
==================

Features
--------

- Lock file dumps are now guarenteed to end with a trailing newline.  `#2 <https://github.com/sarugaku/plette/issues/2>`_


Bug Fixes
---------

- Fix AttributeError in `Lockfile.is_up_to_date()`  `#1 <https://github.com/sarugaku/plette/issues/1>`_

- Fix `Lockfile.dump()` to work correctly on Python 2 when outputting to `io`.  `#2 <https://github.com/sarugaku/plette/issues/2>`_


0.1.0 (2018-08-16)
==================

Initial release.
