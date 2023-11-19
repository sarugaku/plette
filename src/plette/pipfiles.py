import hashlib
import json

import tomlkit

from dataclasses import dataclass, field

from typing import Optional
from .models import (
    Hash, Requires, PipfileSection, Pipenv,
    PackageCollection, ScriptCollection, SourceCollection,
)


PIPFILE_SECTIONS = {
    "source": SourceCollection,
    "packages": PackageCollection,
    "dev-packages": PackageCollection,
    "requires": Requires,
    "scripts": ScriptCollection,
    "pipfile":  PipfileSection,
    "pipenv": Pipenv
}

DEFAULT_SOURCE_TOML = """\
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true
"""

@dataclass
class Pipfile:
    """Representation of a Pipfile."""
    sources: SourceCollection
    packages: Optional[PackageCollection] = None

    def get_hash(self):
        data = {
            "_meta": {
                "sources": getattr(self, "source", {}),
                "requires": getattr(self, "requires", {}),
            },
            "default": getattr(self, "packages", {}),
            "develop": getattr(self, "dev-packages", {}),
        }
        for category, values in self.__dict__.items():
            if category in PIPFILE_SECTIONS or category in ("default", "develop", "pipenv"):
                continue
            data[category] = values
        content = json.dumps(data, sort_keys=True, separators=(",", ":"))
        if isinstance(content, str):
            content = content.encode("utf-8")
        return Hash.from_hash(hashlib.sha256(content))


class Foo:
    source: SourceCollection
    packages: Optional[PackageCollection] = None
    dev_packages: PackageCollection
    requires: Requires
    scripts: ScriptCollection
    pipfile: PipfileSection
    pipenv: Pipenv

    @classmethod
    def load(cls, f, encoding=None):
        content = f.read()
        if encoding is not None:
            content = content.decode(encoding)
        data = tomlkit.loads(content)
        if "source" not in data:
            # HACK: There is no good way to prepend a section to an existing
            # TOML document, but there's no good way to copy non-structural
            # content from one TOML document to another either. Modify the
            # TOML content directly, and load the new in-memory document.
            sep = "" if content.startswith("\n") else "\n"
            content = DEFAULT_SOURCE_TOML + sep + content
        data = tomlkit.loads(content)
        return cls(data)

    def __getitem__(self, key):
        value = self[key]
        try:
            return PIPFILE_SECTIONS[key](value)
        except KeyError:
            return value

    def get_hash(self):
        data = {
            "_meta": {
                "sources": self["source"],
                "requires": getattr(self, "requires", {}),
            },
            "default": getattr(self, "packages", {}),
            "develop": getattr(self, "dev-packages", {}),
        }
        for category, values in self.__dict__.items():
            if category in PIPFILE_SECTIONS or category in ("default", "develop", "pipenv"):
                continue
            data[category] = values
        content = json.dumps(data, sort_keys=True, separators=(",", ":"))
        if isinstance(content, str):
            content = content.encode("utf-8")
        return Hash.from_hash(hashlib.sha256(content))

    def dump(self, f, encoding=None):
        content = tomlkit.dumps(self._data)
        if encoding is not None:
            content = content.encode(encoding)
        f.write(content)

    @property
    def sources(self):
        try:
            return self["source"]
        except KeyError:
            raise AttributeError("sources")

    @sources.setter
    def sources(self, value):
        self["source"] = value

    @property
    def source(self):
        try:
            return self["source"]
        except KeyError:
            raise AttributeError("source")

    @source.setter
    def source(self, value):
        self["source"] = value

    @property
    def packages(self):
        try:
            return self["packages"]
        except KeyError:
            raise AttributeError("packages")

    @packages.setter
    def packages(self, value):
        self["packages"] = value

    @property
    def dev_packages(self):
        try:
            return self["dev-packages"]
        except KeyError:
            raise AttributeError("dev-packages")

    @dev_packages.setter
    def dev_packages(self, value):
        self["dev-packages"] = value

    @property
    def requires(self):
        try:
            return self["requires"]
        except KeyError:
            raise AttributeError("requires")

    @requires.setter
    def requires(self, value):
        self["requires"] = value

    @property
    def scripts(self):
        try:
            return self["scripts"]
        except KeyError:
            raise AttributeError("scripts")

    @scripts.setter
    def scripts(self, value):
        self["scripts"] = value
