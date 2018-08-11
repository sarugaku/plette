import hashlib

import pytest

try:
    import cerberus
except ImportError:
    cerberus = None

from plette import models


def test_hash_from_hash():
    v = hashlib.md5(b"foo")
    h = models.Hash.from_hash(v)
    assert h.name == "md5"
    assert h.value == "acbd18db4cc2f85cedef654fccc4a4d8"


def test_hash_from_line():
    h = models.Hash.from_line("md5:acbd18db4cc2f85cedef654fccc4a4d8")
    assert h.name == "md5"
    assert h.value == "acbd18db4cc2f85cedef654fccc4a4d8"


def test_hash_as_line():
    h = models.Hash({"md5": "acbd18db4cc2f85cedef654fccc4a4d8"})
    assert h.as_line() == "md5:acbd18db4cc2f85cedef654fccc4a4d8"


def test_source_from_data():
    s = models.Source({
        "name": "devpi",
        "url": "https://$USER:$PASS@mydevpi.localhost",
        "verify_ssl": False,
    })
    assert s.name == "devpi"
    assert s.url == "https://$USER:$PASS@mydevpi.localhost"
    assert s.verify_ssl is False


def test_source_as_data_expanded(monkeypatch):
    monkeypatch.setattr("os.environ", {"USER": "user", "PASS": "pa55"})
    s = models.Source({
        "name": "devpi",
        "url": "https://$USER:$PASS@mydevpi.localhost",
        "verify_ssl": False,
    })
    assert s.url_expanded == "https://user:pa55@mydevpi.localhost"


def test_source_as_data_expanded_partial(monkeypatch):
    monkeypatch.setattr("os.environ", {"USER": "user"})
    s = models.Source({
        "name": "devpi",
        "url": "https://$USER:$PASS@mydevpi.localhost",
        "verify_ssl": False,
    })
    assert s.url_expanded == "https://user:$PASS@mydevpi.localhost"


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


@pytest.mark.skipif(cerberus is None, reason="Skip validation without Ceberus")
def test_requires_no_duplicate_python_version():
    data = {"python_version": "8.19", "python_full_version": "8.1.9"}
    with pytest.raises(ValueError) as ctx:
        models.Requires(data)
    assert cerberus.errors.EXCLUDES_FIELD in ctx.value.validator._errors
    assert len(ctx.value.validator._errors) == 2


def test_package_str():
    p = models.Package("*")
    p.version == "*"


def test_package_dict():
    p = models.Package({"version": "*"})
    p.version == "*"


def test_package_wrong_key():
    p = models.Package({"path": ".", "editable": True})
    assert p.editable is True
    with pytest.raises(AttributeError) as ctx:
        p.version
    assert str(ctx.value) == "version"


HASH = "9aaf3dbaf8c4df3accd4606eb2275d3b91c9db41be4fd5a97ecc95d79a12cfe6"


def test_meta():
    m = models.Meta({
        "hash": {"sha256": HASH},
        "pipfile-spec": 6,
        "requires": {},
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": True,
            },
        ],
    })
    assert m.hash.name == "sha256"
