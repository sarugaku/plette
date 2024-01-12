import pytest
from plette.models import Source
from plette import models

def test_source_from_data():
    s = Source(
        **{
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": False,
          }
    )
    assert s.name == "devpi"
    assert s.url == "https://$USER:$PASS@mydevpi.localhost"
    assert s.verify_ssl is False


def test_source_as_data_expanded(monkeypatch):
    monkeypatch.setattr("os.environ", {"USER": "user", "PASS": "pa55"})
    s = Source(
        **{
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": False,
        }
    )
    assert s.url_expanded == "https://user:pa55@mydevpi.localhost"


def test_source_as_data_expanded_partial(monkeypatch):
    monkeypatch.setattr("os.environ", {"USER": "user"})
    s = Source(
        **{
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": False,
        }
    )
    assert s.url_expanded == "https://user:$PASS@mydevpi.localhost"


def test_validation_error():
    data = {"name": "test", "verify_ssl": 1}

    with pytest.raises(TypeError) as exc_info:
        Source(**data)

    error_message = str(exc_info.value)

    assert "missing 1 required positional argument: 'url'" in error_message

    data["url"]  = "http://localhost:8000"

    with pytest.raises(models.ValidationError) as exc_info:
        Source(**data)

    error_message = str(exc_info.value)


    assert "verify_ssl: must be of boolean type" in error_message
