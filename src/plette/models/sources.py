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
    name: str
    url: str
    verify_ssl: bool

    @property
    def url_expanded(self):
        return os.path.expandvars(self.url)
