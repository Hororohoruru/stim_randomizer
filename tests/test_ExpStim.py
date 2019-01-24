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
