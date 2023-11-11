import hashlib

import pytest

from plette import models


def test_requires_python_version():
    r = models.Requires({"python_version": "8.19"})
    assert r.python_version == "8.19"


def test_requires_python_version_no_full_version():
    r = models.Requires({"python_version": "8.19"})
    with pytest.raises(AttributeError) as ctx:
        r.python_full_version
    assert str(ctx.value) == "python_full_version"


def test_requires_python_full_version():
    r = models.Requires({"python_full_version": "8.19"})
    assert r.python_full_version == "8.19"


def test_requires_python_full_version_no_version():
    r = models.Requires({"python_full_version": "8.19"})
    with pytest.raises(AttributeError) as ctx:
        r.python_version
    assert str(ctx.value) == "python_version"


def test_allows_python_version_and_full():
    r = models.Requires({"python_version": "8.1", "python_full_version": "8.1.9"})
    assert r.python_version == "8.1"
    assert r.python_full_version == "8.1.9"


@pytest.fixture()
def sources():
    return models.SourceCollection(
        [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": True,
            },
            {
                "name": "devpi",
                "url": "http://127.0.0.1:$DEVPI_PORT/simple",
                "verify_ssl": True,
            },
        ]
    )


def test_get_slice(sources):
    sliced = sources[:1]
    assert isinstance(sliced, models.SourceCollection)
    assert len(sliced) == 1
    assert sliced[0] == models.Source(
        {
            "name": "pypi",
            "url": "https://pypi.org/simple",
            "verify_ssl": True,
        }
    )


def test_set_slice(sources):
    sources[1:] = [
        {
            "name": "localpi-4433",
            "url": "https://127.0.0.1:4433/simple",
            "verify_ssl": False,
        },
        {
            "name": "localpi-8000",
            "url": "http://127.0.0.1:8000/simple",
            "verify_ssl": True,
        },
    ]
    assert sources == [
        {
            "name": "pypi",
            "url": "https://pypi.org/simple",
            "verify_ssl": True,
        },
        {
            "name": "localpi-4433",
            "url": "https://127.0.0.1:4433/simple",
            "verify_ssl": False,
        },
        {
            "name": "localpi-8000",
            "url": "http://127.0.0.1:8000/simple",
            "verify_ssl": True,
        },
    ]


def test_del_slice(sources):
    del sources[:1]
    assert sources._data == [
        {
            "name": "devpi",
            "url": "http://127.0.0.1:$DEVPI_PORT/simple",
            "verify_ssl": True,
        },
    ]


def test_validation_error():
    data = {"name": "test", "verify_ssl": 1}
    with pytest.raises(models.base.ValidationError) as exc_info:
        models.Source.validate(data)

    error_message = str(exc_info.value)
    assert "verify_ssl: must be of boolean type" in error_message
    assert "url: required field" in error_messgge
