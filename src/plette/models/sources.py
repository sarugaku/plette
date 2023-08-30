# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import os

from dataclasses import dataclass


@dataclass
class Source:
    """Information on a "simple" Python package index.

    This could be PyPI, or a self-hosted index server, etc. The server
    specified by the `url` attribute is expected to provide the "simple"
    package API.
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

    name: str
    url: str
    verify_ssl: bool

    @property
    def url_expanded(self):
        return os.path.expandvars(self.url)
