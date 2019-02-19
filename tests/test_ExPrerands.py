"""
Tests for the ExPrerands class inside core.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import os
import pytest

import pandas as pd

from stim_randomizer.core import ExPrerands

categories = ['animal', 'human', 'nature']


def test_object_is_constructed_correctly(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    if esets.dir_type == 'parent':
        expected_out_dir = os.path.join(esets.root_path,
                                        '../prerands')
    else:
        expected_out_dir = os.path.join(esets.root_path,
                                        'prerands')

    assert esets.out_dir == expected_out_dir


def test_path_is_assignated_correctly(setup_expstim_plain):
    tmpstim = setup_expstim_plain
    esets = ExPrerands(tmpstim.path, tmpstim.subsets, 'parent')

    assert esets.root_path == tmpstim.path


@pytest.mark.rises
def test_get_dir_raises_exception_with_invalid_dir_type(setup_expstim_plain):
    tmpstim = setup_expstim_plain

    with pytest.raises(ValueError):
        ExPrerands(tmpstim.path, tmpstim.subsets, 'cousin')


def test_subset_parser(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    parsed_sets = esets._subset_parser(esets.subsets_path)

    assert len(parsed_sets) == len(os.listdir(esets.subsets_path))