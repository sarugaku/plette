# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member

import json
import numbers

import collections.abc as collections_abc

from dataclasses import dataclass

from .models import DataView, Meta, PackageCollection


class _LockFileEncoder(json.JSONEncoder):
    """A specilized JSON encoder to convert loaded data into a lock file.

    This adds a few characteristics to the encoder:

    * The JSON is always prettified with indents and spaces.
    * The output is always UTF-8-encoded text, never binary, even on Python 2.
    """
    def __init__(self):
        super().__init__(
            indent=4, separators=(",", ": "), sort_keys=True,
        )

    def encode(self, o):
        content = super().encode(o)
        if not isinstance(content, str):
            content = content.decode("utf-8")
        content += "\n"
        return content

    def iterencode(self, o, _one_shot=False):
        for chunk in super().iterencode(o):
            if not isinstance(chunk, str):
                chunk = chunk.decode("utf-8")
            yield chunk
        yield "\n"


PIPFILE_SPEC_CURRENT = 6


def _copy_jsonsafe(value):
    """Deep-copy a value into JSON-safe types.
    """
    if isinstance(value, (str, numbers.Number)):
        return value
    if isinstance(value, collections_abc.Mapping):
        return {str(k): _copy_jsonsafe(v) for k, v in value.items()}
    if isinstance(value, collections_abc.Iterable):
        return [_copy_jsonsafe(v) for v in value]
    if value is None:   # This doesn't happen often for us.
        return None
    return str(value)


@dataclass
class Lockfile:
    """Representation of a Pipfile.lock."""

    _meta: Meta
    default: dict
    develop: dict
    __SCHEMA__ = {
        "_meta": {"type": "dict", "required": True},
        "default": {"type": "dict", "required": True},
        "develop": {"type": "dict", "required": True},
    }


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

    @classmethod
    def load(cls, fh, encoding=None):
        if encoding is None:
            data = json.load(fh)
        else:
            data = json.loads(fh.read().decode(encoding))
        return cls(data)

    @classmethod
    def with_meta_from(cls, pipfile, categories=None):
        data = {
            "_meta": {
                "hash": _copy_jsonsafe(pipfile.get_hash()._data),
                "pipfile-spec": PIPFILE_SPEC_CURRENT,
                "requires": _copy_jsonsafe(pipfile._data.get("requires", {})),
                "sources": _copy_jsonsafe(pipfile.sources._data),
            },
        }
        if categories is None:
            data["default"] = _copy_jsonsafe(pipfile._data.get("packages", {}))
            data["develop"] = _copy_jsonsafe(pipfile._data.get("dev-packages", {}))
        else:
            for category in categories:
                if category == "default" or category == "packages":
                    data["default"] = _copy_jsonsafe(pipfile._data.get("packages", {}))
                elif category == "develop" or category == "dev-packages":
                    data["develop"] = _copy_jsonsafe(pipfile._data.get("dev-packages", {}))
                else:
                    data[category] = _copy_jsonsafe(pipfile._data.get(category, {}))
        if "default" not in data:
            data["default"]  = {}
        if "develop" not in data:
            data["develop"] = {}
        return cls(data)

    def __getitem__(self, key):
        value = self._data[key]
        try:
            if key == "_meta":
                return Meta(value)
            else:
                return PackageCollection(value)
        except KeyError:
            return value

    def __setitem__(self, key, value):
        if isinstance(value, DataView):
            self._data[key] = value._data
        else:
            self._data[key] = value

    def is_up_to_date(self, pipfile):
        return self.meta.hash == pipfile.get_hash()

    def dump(self, fh, encoding=None):
        encoder = _LockFileEncoder()
        if encoding is None:
            for chunk in encoder.iterencode(self._data):
                fh.write(chunk)
        else:
            content = encoder.encode(self._data)
            fh.write(content.encode(encoding))

    @property
    def meta(self):
        try:
            return self["_meta"]
        except KeyError:
            raise AttributeError("meta")

    @meta.setter
    def meta(self, value):
        self["_meta"] = value

    @property
    def _meta(self):
        try:
            return self["_meta"]
        except KeyError:
            raise AttributeError("meta")

    @_meta.setter
    def _meta(self, value):
        self["_meta"] = value

    @property
    def default(self):
        try:
            return self["default"]
        except KeyError:
            raise AttributeError("default")

    @default.setter
    def default(self, value):
        self["default"] = value

    @property
    def develop(self):
        try:
            return self["develop"]
        except KeyError:
            raise AttributeError("develop")

    @develop.setter
    def develop(self, value):
        self["develop"] = value
