# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member
from dataclasses import dataclass


@dataclass
class Hash:

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
    value: str

    def validate_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Hash.name must be a string")

        return value

    def validate_value(self, value):
        if not isinstance(value, str):
            raise ValueError("Hash.value must be a string")

        return value

    @classmethod
    def from_hash(cls, ins):
        """Interpolation to the hash result of `hashlib`.
        """
        return cls(name=ins.name, value=ins.hexdigest())

    @classmethod
    def from_line(cls, value):
        """parse a dependecy line and create a Hash object"""
        try:
            name, value = value.split(":", 1)
        except ValueError:
            name = "sha256"
        return cls(name, value)

    def __eq__(self, other):
        if not isinstance(other, Hash):
            raise TypeError(f"cannot compare Hash with {type(other).__name__!r}")
        return self.value == other.value

    def as_line(self):
        return f"{self.name}:{self.value}"
