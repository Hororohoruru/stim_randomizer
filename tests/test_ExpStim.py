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
def setup_plain_dir():
    test_dir = tempfile.mkdtemp()

    for i in range(10):
        tempfile.mkstemp(dir=test_dir)

    return test_dir


@pytest.fixture()
def setup_cat(setup_cat_dir):

    test_obj = ExpStim(str(setup_cat_dir), categories)

    return test_obj


@pytest.fixture()
def setup_plain(setup_plain_dir):

    test_obj = ExpStim(str(setup_plain_dir))

    return test_obj


def test_instantiation_categories(setup_cat):
    es = setup_cat

    assert isinstance(es, ExpStim)
    assert sorted(es.categories) == sorted(categories)


def test_instantiation_plain(setup_plain):
    es = setup_plain

    assert isinstance(es, ExpStim)
    assert es.categories is None


def test_class_scanner_and_path(setup_cat_dir):
    tmpdir = str(setup_cat_dir)
    es = ExpStim(tmpdir)

    assert es.path == tmpdir
    assert isinstance(es, ExpStim)
    assert sorted(es.categories) == sorted(categories)
    assert sorted(es.scan_categories()) == sorted(categories)


def test_no_subsets_or_prerands_by_default(setup_cat):
    es = setup_cat

    assert es.subsets is None
    assert es.prerands is None
