import glob

import pytest

import plette
from plette import Pipfile

invalid_files = glob.glob("examples/*invalid*")
valid_files = glob.glob("examples/*ok*")

@pytest.mark.parametrize("fname", invalid_files)
def test_invalid_files(fname):
    
    with pytest.raises(plette.models.base.ValidationError):
        with open(fname) as f:
            pipfile = Pipfile.load(f)


@pytest.mark.parametrize("fname", valid_files)
def test_valid_files(fname):

    with open(fname) as f:
        pipfile = Pipfile.load(f)
