# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-member

import dataclasses
import json
import numbers

import collections.abc as collections_abc

from dataclasses import dataclass, field, asdict
from typing import Optional

from .models import DataModel, Meta, PackageCollection


class _LockFileEncoder(json.JSONEncoder):
    """A specilized JSON encoder to convert loaded data into a lock file.

    This adds a few characteristics to the encoder:

    * The JSON is always prettified with indents and spaces.
    * The output is always UTF-8-encoded text, never binary, even on Python 2.
    """
    def __init__(self):
        super(_LockFileEncoder, self).__init__(
            indent=4, separators=(",", ": "), sort_keys=True,
        )

    def encode(self, obj):
        content = super(_LockFileEncoder, self).encode(obj)
        if not isinstance(content, str):
            content = content.decode("utf-8")
        content += "\n"
        return content

    def iterencode(self, obj):
        for chunk in super(_LockFileEncoder, self).iterencode(obj):
            if not isinstance(chunk, str):
                chunk = chunk.decode("utf-8")
            yield chunk
        yield "\n"


PIPFILE_SPEC_CURRENT = 6


def flatten_versions(d):
    copy = {}
    # Iterate over a copy of the dictionary
    for key, value in d.items():
        # If the key is "version", replace the key with the value
        copy[key] = value["version"]
    return copy


class DCJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            o = dataclasses.asdict(o)
            if "_meta" in o:
                o["_meta"]["pipfile-spec"] = o["_meta"].pop("pipfile_spec")
                o["_meta"]["hash"] = {o["_meta"]["hash"]["name"]: o["_meta"]["hash"]["value"]}
                o["_meta"]["sources"] = o["_meta"]["sources"].pop("sources")

            remove_empty_values(o)

            for section in ["default", "develop"]:
                try:
                    o[section] = flatten_versions(o[section])
                except KeyError:
                    continue
            # add silly default values
            if "develop" not in o:
                o["develop"] = {}
            if "requires" not in o["_meta"]:
                o["_meta"]["requires"] = {}
            return o
        return super().default(o)


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


class Lockfile(DataModel):
    """Representation of a Pipfile.lock.
    """
    __SCHEMA__ = {
        "_meta": {"type": "dict", "required": True},
        "default": {"type": "dict", "required": True},
        "develop": {"type": "dict", "required": True},
    }

    @classmethod
    def validate(cls, data):
        for key, value in data.items():
            if key == "_meta":
                Meta.validate(value)
            else:
                PackageCollection.validate(value)

    @classmethod
    def load(cls, f, encoding=None):
        if encoding is None:
            data = json.load(fh)
        else:
            data = json.loads(fh.read().decode(encoding))
        return cls(**data)

    @classmethod
    def with_meta_from(cls, pipfile, categories=None):
        data = {
            "_meta": {
                "hash": pipfile.get_hash().__dict__,
                "pipfile-spec": PIPFILE_SPEC_CURRENT,
                "requires": _copy_jsonsafe(getattr(pipfile, "requires", {})),
            },
        }

        data["_meta"].update(asdict(pipfile.sources))

        if categories is None:
            data["default"] = _copy_jsonsafe(getattr(pipfile, "packages", {}))
            data["develop"] = _copy_jsonsafe(getattr(pipfile, "dev-packages", {}))
        else:
            for category in categories:
                if category in ["default", "packages"]:
                    data["default"] = _copy_jsonsafe(getattr(pipfile,"packages", {}))
                elif category in ["develop", "dev-packages"]:
                    data["develop"] = _copy_jsonsafe(
                            getattr(pipfile,"dev-packages", {}))
                else:
                    data[category] = _copy_jsonsafe(getattr(pipfile, category, {}))
        if "default" not in data:
            data["default"] = {}
        if "develop" not in data:
            data["develop"] = {}
        return cls(data)

    def __getitem__(self, key):
        value = self[key]
        try:
            if key == "_meta":
                return Meta(**value)
            return PackageCollection(value)
        except KeyError:
            return value

    def is_up_to_date(self, pipfile):
        return self.meta.hash == pipfile.get_hash()

    def dump(self, fh):
        json.dump(self, fh, cls=DCJSONEncoder)
        self.meta = self._meta

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = value
