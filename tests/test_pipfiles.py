import datetime
import textwrap

import pytest

from plette import Pipfile
from plette.models import PackageCollection, SourceCollection
from plette.models.sections import Pipenv
from plette.models.base import DataValidationError


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
    assert section._data == [
        {
            "name": "devpi",
            "url": "https://$USER:$PASS@mydevpi.localhost",
            "verify_ssl": True,
        },
    ]


def test_package_section():
    section = PackageCollection({
        "flask": {"version": "*"},
        "jinja2": "*",
    })
    assert section["jinja2"].version == "*"
    with pytest.raises(KeyError) as ctx:
        section["mosql"]
    assert str(ctx.value) == repr("mosql")


def test_pipfile_load(tmpdir):
    fi = tmpdir.join("Pipfile.in")
    fi.write(textwrap.dedent("""
        [packages]
        flask = { version = "*" }
        jinja2 = '*'   # A comment.
    """))
    p = Pipfile.load(fi)
    assert p["source"] == SourceCollection([
        {
            'url': 'https://pypi.org/simple',
            'verify_ssl': True,
            'name': 'pypi',
        },
    ])
    assert p["packages"] == PackageCollection({
        "flask": {"version": "*"},
        "jinja2": "*",
    })


def test_cool_down_period_valid():
    section = Pipenv({"cool-down-period": "30d"})
    assert section.cool_down_period == "30d"
    assert section.cool_down_period_timedelta == datetime.timedelta(days=30)


def test_cool_down_period_none():
    section = Pipenv({})
    assert section.cool_down_period is None
    assert section.cool_down_period_timedelta is None


def test_cool_down_period_invalid():
    with pytest.raises(DataValidationError):
        Pipenv({"cool-down-period": "30days"})
    with pytest.raises(DataValidationError):
        Pipenv({"cool-down-period": "abc"})
    with pytest.raises(DataValidationError):
        Pipenv({"cool-down-period": 30})


def test_cool_down_period_setter():
    section = Pipenv({})
    section.cool_down_period = "7d"
    assert section.cool_down_period == "7d"
    assert section.cool_down_period_timedelta == datetime.timedelta(days=7)


def test_cool_down_period_setter_invalid():
    section = Pipenv({})
    with pytest.raises(DataValidationError):
        section.cool_down_period = "7days"


def test_cool_down_period_in_pipfile(tmpdir):
    fi = tmpdir.join("Pipfile.in")
    fi.write(textwrap.dedent("""
        [pipenv]
        cool-down-period = "30d"
    """))
    p = Pipfile.load(fi)
    pipenv_section = p["pipenv"]
    assert pipenv_section.cool_down_period == "30d"
    assert pipenv_section.cool_down_period_timedelta == datetime.timedelta(days=30)


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
    p["source"][0].verify_ssl = False

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
