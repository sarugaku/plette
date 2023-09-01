import pytest

from plette.models import Package

def test_package_str():
    p = Package("*")
    p.version == "*"


def test_package_dict():
    p = Package({"version": "*"})
    p.version == "*"


def test_package_wrong_key():
    p = Package({"path": ".", "editable": True})
    assert p.editable is True
    with pytest.raises(AttributeError) as ctx:
        p.version
    assert str(ctx.value) == "version"


def test_package_with_wrong_extras():
    with pytest.raises(models.base.ValidationError):
        p = Package({"version": "==1.20.0", "extras": "broker"})


def test_package_with_extras():
    p = Package(**{"version": "==1.20.0", "extras": ["broker", "tests"]})
    assert p.extras == ['broker', 'tests']


