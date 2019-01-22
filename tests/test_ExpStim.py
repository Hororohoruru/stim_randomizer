"""
Tests for ExpStim.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import json
import os
import glob
import pytest
import shutil
import tempfile

import numpy as np
import pandas as pd

from pprint import pprint

from stim_randomizer.ExpStim import ExpStim


categories = ['animal', 'human', 'nature']


@pytest.fixture()
def setup_cat_dir():
    test_dir = tempfile.mkdtemp()

    for category in categories:
        for i in range(10):
            tempfile.mkstemp(prefix=(category + '_%02d' % i), dir=test_dir)

    return test_dir


@pytest.fixture()
def setup_cat_class(setup_cat_dir):

    test_obj = ExpStim(str(setup_cat_dir))

    return test_obj


def test_path(setup_cat_class):

    test_ExpStim = setup_cat_class

    assert test_ExpStim.path == test_ExpStim.path
    assert sorted(test_ExpStim.categories) == sorted(categories)
    assert test_ExpStim.subsets is None