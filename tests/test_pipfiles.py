import textwrap

from plette import Pipfile
from plette.models import PackageCollection, SourceCollection


def test_source_section():
    section = SourceCollection([
        {
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": False,
        },
    ])
    assert len(section) == 1
    assert section[0].url == "https://$USER:$PASS@mydevpi.localhost"


def test_source_section_transparent():
    section = SourceCollection([
        {
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": False,
        },
    ])
    section[0].verify_ssl = True
    assert section == SourceCollection([
        {
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": True,
        },
    ])


def test_package_section():
    section = PackageCollection({
        "flask": {"version": "*"},
        "jinja2": "*",
    })
    assert section.packages["jinja2"].version == "*"


def test_pipfile_load(tmpdir):
    fi = tmpdir.join("Pipfile.in")
    fi.write(textwrap.dedent("""
        [packages]
        flask = { version = "*" }
        jinja2 = '*'   # A comment.
    """))
    p = Pipfile.load(fi)

    assert p.source == SourceCollection([
        {
            'url': 'https://pypi.org/simple',
            'verify_ssl': True,
            'name': 'pypi',
        },
    ])
    assert p.packages == {
        "flask": {"version": "*"},
        "jinja2": "*",
    }


def test_pipfile_preserve_format(tmpdir):
    fi = tmpdir.join("Pipfile.in")
    fi.write(textwrap.dedent(
        """\
        [packages]
        flask = { version = "*" }
        jinja2 = '*'
        """,
    ))
    p = Pipfile.load(fi)
    p.source.verify_ssl = False

    fo = tmpdir.join("Pipfile.out")
    p.dump(fo)
    assert fo.read() == textwrap.dedent(
        """\
        [[source]]
        name = "pypi"
        url = "https://pypi.org/simple"
        verify_ssl = false

        [packages]
        flask = { version = "*" }
        jinja2 = '*'
        """,
    )
