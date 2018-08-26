===============
Validating Data
===============

Plette provides optional validation for input data. This chapter discusses
how validation works.


Setting up Validation
=====================

Validation is provided by the Cerberus_ library. You can install it along with
Plette manually, or by specifying the “validation” extra when installing
Plette:

.. code-block:: none

    pip install plette[validation]

Plette automatically enables validation when Cerberus is available.

.. _Cerberus: http://docs.python-cerberus.org/


Validating Data
===============

Data is validated on input (or when a model is loaded). ``ValidationError`` is
raised when validation fails::

    >>> plette.models.Source({})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "plette/models/base.py", line 37, in __init__
        self.validate(data)
      File "plette/models/base.py", line 67, in validate
        return validate(cls, data)
      File "plette/models/base.py", line 27, in validate
        raise ValidationError(data, v)
    plette.models.base.ValidationError: {}

This exception class has a ``validator`` member to allow you to access the
underlying Cerberus validator, so you can know what exactly went wrong::

    >>> try:
    ...     plette.models.Source({'verify_ssl': True})
    ... except plette.models.ValidationError as e:
    ...     for error in e.validator._errors:
    ...         print(error.schema_path)
    ...
    ('name', 'required')
    ('url', 'required')

See `Ceberus’s error handling documentation`_ to know how the errors are
represented and reported.

.. _`Ceberus’s error handling documentation`: http://docs.python-cerberus.org/en/stable/errors.html
