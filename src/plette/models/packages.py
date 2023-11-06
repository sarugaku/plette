# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PackageSpecfiers:
    extras: List[str]


@dataclass
class Package:

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

    version: Optional[str] = None
    specifiers: Optional[PackageSpecfiers] = None
    editable: Optional[bool] = None
    extras: Optional[PackageSpecfiers] = None
    path: Optional[str] = None

    def validate_extras(self, value, field):
        if value is None:
            return value
        if not (isinstance(value, list) and all(isinstance(i, str) for i in value)):
            raise ValueError("Extras must be a list or None")
        return value
