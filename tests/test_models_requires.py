import pytest
from plette import models

def test_requires_python_version():
    r = models.Requires(**{"python_version": "8.19"})
    assert r.python_version == "8.19"


def test_requires_python_version_no_full_version():
    r = models.Requires(**{"python_version": "8.19"})
    r.python_full_version is None


def test_requires_python_full_version():
    r = models.Requires(**{"python_full_version": "8.19"})
    assert r.python_full_version == "8.19"


def test_requires_python_full_version_no_version():
    r = models.Requires(**{"python_full_version": "8.19"})
    r.python_version is None


def test_allows_python_version_and_full():
    r = models.Requires(**{"python_version": "8.1", "python_full_version": "8.1.9"})
    assert r.python_version == "8.1"
    assert r.python_full_version == "8.1.9"
