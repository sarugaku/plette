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
        for v in value:
            Source(**v)
        return value

@dataclass
class Requires:

    python_version: Optional[str]
    python_version: Optional[str]


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
