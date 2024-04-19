import glob

import pytest

import plette
from plette import Pipfile

from plette.models.base import ValidationError
invalid_files = glob.glob("examples/*invalid*")
valid_files = glob.glob("examples/*ok*")

@pytest.mark.parametrize("fname", invalid_files)
def test_invalid_files(fname):
    with pytest.raises((ValueError, plette.models.base.ValidationError, ValidationError)) as excinfo:
        with open(fname) as f:
            pipfile = Pipfile.load(f)


@pytest.mark.parametrize("fname", valid_files)
def test_valid_files(fname):

    with open(fname) as f:
        pipfile = Pipfile.load(f)
