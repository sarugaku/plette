import pytest

from plette.models import Package


def test_package_dict():
    p = Package(**{"name": "numpy", "version": "*"})
    assert p.version == "*"


def test_package_version_is_none():
    p = Package(**{"name": "scipy", "path": ".", "editable": True})
    assert p.version == "*"
    assert p.editable is True

def test_package_with_wrong_extras():
    with pytest.raises(ValueError):
        p = Package(**{"name": "simpy", "version": "==1.20.0", "extras": "broker"})

    with pytest.raises(ValueError):
        p = Package(**{"name":"erroR", "version": "==1.20.0", "extras": ["broker", {}]})

    with pytest.raises(ValueError):
        p = Package(**{"name": "erroR", "version": "==1.20.0", "extras": ["broker", 1]})


def test_package_with_extras():
    p = Package(**{"name": "pynki", "version":"==1.20.0", "extras": ["broker", "tests"]})
    assert p.extras == ['broker', 'tests']


def test_package_without_version():
    p = Package(**{"name": "pleasePinYourPackages", "path": ".", "editable": True})
    assert p.editable is True
    assert p.version is "*"
