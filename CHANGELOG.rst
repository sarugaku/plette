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

No significant changes.
