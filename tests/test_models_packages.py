import pytest

from plette.models import Package

def test_package_str():
    p = Package("*")
    p.version == "*"


def test_package_dict():
    p = Package(**{"version": "*"})
    p.version == "*"


def test_package_version_is_none():
    p = Package(**{"path": ".", "editable": True})
    assert p.version == None
    assert p.editable is True

def test_package_with_wrong_extras():
    with pytest.raises(ValueError):
        p = Package(**{"version": "==1.20.0", "extras": "broker"})

    with pytest.raises(ValueError):
        p = Package(**{"version": "==1.20.0", "extras": ["broker", {}]})

    with pytest.raises(ValueError):
        p = Package(**{"version": "==1.20.0", "extras": ["broker", 1]})


def test_package_with_extras():
    p = Package(**{"version": "==1.20.0", "extras": ["broker", "tests"]})
    assert p.extras == ['broker', 'tests']