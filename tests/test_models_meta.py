from plette.models import Meta

HASH = "9aaf3dbaf8c4df3accd4606eb2275d3b91c9db41be4fd5a97ecc95d79a12cfe6"

def test_meta():
    m = Meta.from_dict(
        {
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
          }
    )
    assert m.hash.name == "sha256"
