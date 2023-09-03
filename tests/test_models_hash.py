import hashlib

from plette.models.hashes import Hash

def test_hash_from_hash():
    v = hashlib.md5(b"foo")
    h = Hash.from_hash(v)
    assert h.name == "md5"
    assert h.value == "acbd18db4cc2f85cedef654fccc4a4d8"


def test_hash_from_line():
    h = Hash.from_line("md5:acbd18db4cc2f85cedef654fccc4a4d8")
    assert h.name == "md5"
    assert h.value == "acbd18db4cc2f85cedef654fccc4a4d8"


def test_hash_as_line():
    h = Hash(name="md5", value="acbd18db4cc2f85cedef654fccc4a4d8")
    assert h.as_line() == "md5:acbd18db4cc2f85cedef654fccc4a4d8"
