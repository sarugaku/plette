from dataclasses import dataclass
from typing import Optional

from .base import DataView


@dataclass
class PackageSpecfiers:
    version: str
    extras: list

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
    extras: Optional[list] = None
