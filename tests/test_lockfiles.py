# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
import json
import textwrap

from plette import Lockfile, Pipfile
from plette.models import Package, SourceCollection, Hash, Requires


HASH = "9aaf3dbaf8c4df3accd4606eb2275d3b91c9db41be4fd5a97ecc95d79a12cfe6"


def test_lockfile_load_sources(tmpdir):
    fi = tmpdir.join("in.json")
    fi.write(textwrap.dedent(
        """\
        {
            "_meta": {
                "hash": {"sha256": "____hash____"},
                "pipfile-spec": 6,
                "requires": {},
                "sources": [
                    {
                        "name": "pypi",
                        "url": "https://pypi.org/simple",
                        "verify_ssl": true
                    }
                ]
            },
            "default": {
                "flask": {"version": "*"},
                "jinja2": "*"
            },
            "develop": {}
        }
        """,
    ).replace("____hash____", HASH))
    lock = Lockfile.load(fi)
    assert lock.meta.sources == SourceCollection([
        {
            'url': 'https://pypi.org/simple',
            'verify_ssl': True,
            'name': 'pypi',
        },
    ])


def test_lockfile_load_sources_package_spec(tmpdir):
    fi = tmpdir.join("in.json")
    fi.write(textwrap.dedent(
        """\
        {
            "_meta": {
                "hash": {"sha256": "____hash____"},
                "pipfile-spec": 6,
                "requires": {},
                "sources": [
                    {
                        "name": "pypi",
                        "url": "https://pypi.org/simple",
                        "verify_ssl": true
                    }
                ]
            },
            "default": {
                "flask": {"version": "*"},
                "jinja2": "*"
            },
            "develop": {}
        }
        """,
    ).replace("____hash____", HASH))
    lock = Lockfile.load(fi)
    assert lock.default["jinja2"] == Package("*")


def test_lockfile_dump_format(tmpdir):
    content = textwrap.dedent(
        """\
        {
            "_meta": {
                "hash": {
                    "sha256": "____hash____"
                },
                "pipfile-spec": 6,
                "requires": {},
                "sources": [
                    {
                        "name": "pypi",
                        "url": "https://pypi.org/simple",
                        "verify_ssl": true
                    }
                ]
            },
            "default": {
                "flask": {
                    "version": "*"
                },
                "jinja2": "*"
            },
            "develop": {}
        }
        """,
    ).replace("____hash____", HASH)

    fi = tmpdir.join("in.json")
    fi.write(content)
    lock = Lockfile.load(fi)

    # Don't use `lock.dump(outpath)`. It has some flushing issues.
    outpath = tmpdir.join("out.json")
    with outpath.open("w") as f:
        lock.dump(f)
    loaded = json.loads(outpath.read())
    assert "_meta" in loaded
    assert json.loads(outpath.read()) == json.loads(content)


def test_lockfile_from_pipfile_meta():
    pipfile = Pipfile(**{
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": True,
            },
        ],
        "requires": {
            "python_version": "3.7",
        }
    })

    pipfile_hash_value = pipfile.get_hash().value
    lockfile = Lockfile.with_meta_from(pipfile)

    pipfile.requires["python_version"] = "3.8"
    pipfile.sources.sources.append({
        "name": "devpi",
        "url": "http://localhost/simple",
        "verify_ssl": True,
    })

    assert lockfile.meta.hash == Hash.from_dict({"sha256": pipfile_hash_value})
    assert lockfile.meta.requires == Requires(python_version={'python_version': '3.7'}, python_full_version=None)
    assert lockfile.meta.sources == SourceCollection([
        {
            "name": "pypi",
            "url": "https://pypi.org/simple",
            "verify_ssl": True,
        },
    ])
