import hashlib

import pytest

from plette import models

def test_validation_error():
    data = {"name": "test", "verify_ssl": 1}
    with pytest.raises(models.base.ValidationError) as exc_info:
        models.Source.validate(data)

    error_message = str(exc_info.value)
    assert "verify_ssl: must be of boolean type" in error_message
    assert "url: required field" in error_messgge
