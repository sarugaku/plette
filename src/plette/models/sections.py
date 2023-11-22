# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member

from dataclasses import dataclass
from typing import Optional, List

from .hashes import Hash
from .packages import Package
from .scripts import Script
from .sources import Source


@dataclass
class PackageCollection:
    packages: List[Package]

    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if (method := getattr(self, f"validate_{name}", None)):
                setattr(self, name, method(getattr(self, name), field=field))

    def validate_packages(self, value, field):
        packages = {k:Package(v) for k, v in value.items()}
        return packages

@dataclass
class ScriptCollection:
    scripts: List[Script]

@dataclass
class SourceCollection:

    sources: List[Source]

    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if (method := getattr(self, f"validate_{name}", None)):
                setattr(self, name, method(getattr(self, name), field=field))

    def validate_sources(self, value, field):
        sources = []
        for v in value:
            if isinstance(v, dict):
                sources.append(Source(**v))
            elif isinstance(v, Source):
                sources.append(v)
        return sources

    def __iter__(self):
        return (d for d in self.sources)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SourceCollection(self.sources[key])
        if isinstance(key, int):
            src = self.sources[key]
            if isinstance(src, dict):
                return Source(**key)
            if isinstance(src, Source):
                return src
        raise TypeError(f"Unextepcted type {type(src)}")

    def __len__(self):
        return len(self.sources)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self.sources[key] = value
        elif isinstance(value, Source):
            self.sources.append(value)
        elif isinstance(value, list):
            self.sources.extend(value)
        else:
            raise TypeError(f"Unextepcted type {type(value)} for {value}")

    def __delitem__(self, key):
        del self.sources[key]


@dataclass
class Requires:
    python_version: Optional[str] = None
    python_full_version: Optional[str] = None



META_SECTIONS = {
    "hash": Hash,
    "requires": Requires,
    "sources": SourceCollection,
}


@dataclass
class PipfileSection:

    """
    Dummy pipfile validator that needs to be completed in a future PR
    Hint: many pipfile features are undocumented in  pipenv/project.py
    """
    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if (method := getattr(self, f"validate_{name}", None)):
                setattr(self, name, method(getattr(self, name), field=field))


@dataclass
class Meta:

    hash: Hash
    pipfile_spec: str
    requires: Requires
    sources: SourceCollection

    @classmethod
    def from_dict(cls, d: dict) -> "Meta":
        return cls(**{k.replace('-', '_'): v for k, v in d.items()})

    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if (method := getattr(self, f"validate_{name}", None)):
                setattr(self, name, method(getattr(self, name), field=field))

    def validate_hash(self, value, field):
        try:
            return Hash(**value)
        except TypeError:
            return Hash.from_line(value)

    def validate_requires(self, value, field):
        return Requires(value)

    def validate_sources(self, value, field):
        return SourceCollection(value)

    def validate_pipfile_spec(self, value, field):
        if int(value) != 6:
            raise ValueError('Only pipefile-spec version 6 is supported')
        return value


@dataclass
class Pipenv:
    """Represent the [pipenv] section in Pipfile"""

    allow_prereleases: Optional[bool]
