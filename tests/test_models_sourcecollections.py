import hashlib

import pytest

from plette import models
from plette.models import Source, SourceCollection


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
        **{
            "name": "pypi",
            "url": "https://pypi.org/simple",
            "verify_ssl": True,
        }
    )


def test_set_slice(sources):
    sources[1:] = [
        Source(**{
            "name": "localpi-4433",
            "url": "https://127.0.0.1:4433/simple",
            "verify_ssl": False,
        }),
        Source(**{
            "name": "localpi-8000",
            "url": "http://127.0.0.1:8000/simple",
            "verify_ssl": True,
        }),
    ]
    assert sources == \
        SourceCollection([
        Source(**{
            "name": "pypi",
            "url": "https://pypi.org/simple",
            "verify_ssl": True,
        }),
        Source(**{
            "name": "localpi-4433",
            "url": "https://127.0.0.1:4433/simple",
            "verify_ssl": False,
        }),
        Source(**{
            "name": "localpi-8000",
            "url": "http://127.0.0.1:8000/simple",
            "verify_ssl": True,
        }),
        ])


def test_del_slice(sources):
    del sources[:1]
    assert sources == SourceCollection([
        Source(**{
            "name": "devpi",
            "url": "http://127.0.0.1:$DEVPI_PORT/simple",
            "verify_ssl": True,
        }),
    ])
