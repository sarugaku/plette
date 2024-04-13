"""
As pipenv is the main consumer of plette we test all current usage of plette
as used by pipenv.
"""

import plette

# $ git grep plette
# pipenv/project.py:        plette.pipfiles.DEFAULT_SOURCE_TOML = default_sources_toml
# pipenv/project.py:                lockfile = plette.Lockfile.with_meta_from(
# pipenv/project.py:                    plette.Pipfile.load(pf), categories=categories
# pipenv/project.py:        from .vendor.plette.lockfiles import PIPFILE_SPEC_CURRENT
# pipenv/project.py:                default_lockfile = plette.Lockfile.with_meta_from(
# pipenv/project.py:                    plette.Pipfile.load(pf), categories=[]
# pipenv/project.py:            p = plette.Pipfile.load(pf)
# pipenv/routines/check.py:from pipenv.vendor import click, plette
# pipenv/routines/check.py:    p = plette.Pipfile.load(open(project.pipfile_location))
# pipenv/routines/check.py:    p = plette.Lockfile.with_meta_from(p)
# pipenv/utils/locking.py:from pipenv.vendor.plette import lockfiles
# pipenv/utils/pipfile.py:from pipenv.vendor.plette import pipfiles
# pipenv/utils/toml.py:from pipenv.vendor.plette.models import Package, PackageCollection
# pipenv/vendor/vendor.txt:plette==0.4.4
# tests/integration/test_install_misc.py:plette = {{file = "{file_uri}", extras = ["validation"]}}
# tests/integration/test_install_misc.py:        assert "plette" in p.lockfile["default"]
# tests/integration/test_project.py:from pipenv.vendor.plette import Pipfile


def test_has_default_source_toml():
    from plette import pipfiles
    assert hasattr(pipfiles, 'DEFAULT_SOURCE_TOML')


def test_lockfile_with_meta_from():
    """
with plette 0.4.4
pipfile
Pipfile({'source': [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}], 'packages': {'msal': {'version': '==1.20.0', 'extras': ['broker']}}})
>>> from plette import lockfiles
>>> lockfiles.Lockfile.with_meta_from(pipfile)
Lockfile({'_meta': {'hash': {'sha256': 'd94770beebfa823964b540a8e5a3593dd1c7b3120d78033024ee41808a08364e'}, 'pipfile-spec': 6, 'requires': {}, 'sources': [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}]}, 'default': {'msal': {'version': '==1.20.0', 'extras': ['broker']}}, 'develop': {}})
>>> lockfile =  lockfiles.Lockfile.with_meta_from(pipfile)
>>> lockfile._data
{'_meta': {'hash': {'sha256': 'd94770beebfa823964b540a8e5a3593dd1c7b3120d78033024ee41808a08364e'}, 'pipfile-spec': 6, 'requires': {}, 'sources': [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}]}, 'default': {'msal': {'version': '==1.20.0', 'extras': ['broker']}}, 'develop': {}}
"""
    categories = None
    with open("examples/Pipfile.ok.extras-list", encoding="utf-8") as pf:
        lockfile = plette.Lockfile.with_meta_from(
            plette.Pipfile.load(pf), categories=categories
            )
    lockfiledata = lockfile._data

    assert lockfiledata == {'_meta':
                            {'hash': {'sha256': 'd94770beebfa823964b540a8e5a3593dd1c7b3120d78033024ee41808a08364e'},
                             'pipfile-spec': 6,
                             'requires': {},
                             'sources': [{'name': 'pypi', 'url': 'https://pypi.org/simple', 'verify_ssl': True}]
                             },
                            'default': {'msal': {'version': '==1.20.0', 'extras': ['broker']}},
                            'develop': {}
                            }

    categories = ["documentation", "testing"]
