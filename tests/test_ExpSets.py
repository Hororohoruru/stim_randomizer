"""
Tests for the ExpStim class inside core.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import glob
import os
import pytest

import pandas as pd

from stim_randomizer.core import ExpSets

categories = ['animal', 'human', 'nature']


def test_object_is_constructed_correctly(setup_expsets_cat):
    esets = setup_expsets_cat

    if esets.dir_type == 'parent':
        expected_out_dir = os.path.join(esets.root_path,
                                        '../subsets')
    else:
        expected_out_dir = os.path.join(esets.root_path,
                                        'subsets')

    assert esets.out_dir == expected_out_dir


def test_path_is_assignated_correctly(setup_cat_dir):
    tmpdir = str(setup_cat_dir)
    esets = ExpSets(tmpdir, 'parent')

    assert esets.root_path == tmpdir


@pytest.mark.rises
def test_get_dir_raises_exception_with_invalid_dir_type(setup_cat_dir):
    path = setup_cat_dir

    with pytest.raises(ValueError):
        ExpSets(path, 'cousin')


@pytest.mark.rises
@pytest.mark.parametrize('set_num', [9,
                                     pytest.param(10, marks=pytest.mark.xfail)])
def test_create_subsets_raises_exception_when_impossible_to_divide_sets(setup_expsets_cat, set_num):
    esets = setup_expsets_cat

    with pytest.raises(ValueError):
        esets.create_subsets(set_num, categories)


@pytest.mark.rises
def test_create_subsets_raises_exception_when_categories_are_none(setup_expsets_cat):
    esets = setup_expsets_cat

    with pytest.raises(TypeError):
        esets.create_subsets(10, None)


def test_create_subsets_creates_correct_number_of_subsets(setup_expsets_cat):
    esets = setup_expsets_cat
    expected_subset_number = 10

    esets.create_subsets(expected_subset_number, categories)

    subset_number = len(sorted(os.listdir(esets.out_dir)))

    assert expected_subset_number == subset_number


def test_subsets_have_correct_amount_of_files(setup_expsets_cat):
    esets = setup_expsets_cat

    esets.create_subsets(10, categories)

    total_stim = len(sorted([file for file in os.listdir(esets.root_path) if 'subsets' not in file]))
    expected_stim_per_set = total_stim // 10
    subsets = sorted(os.listdir(esets.out_dir))

    for subset in subsets:

        subset_path = os.path.join(esets.out_dir, subset)

        subset_df = pd.read_table(subset_path, header=None)

        assert expected_stim_per_set == len(subset_df)

        for category in categories:

            assert len(subset_df[subset_df[0].str.contains(category)]) == expected_stim_per_set / len(categories)
