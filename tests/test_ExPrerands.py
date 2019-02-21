"""
Tests for the ExPrerands class inside core.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import os
import pytest

import numpy as np
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


@pytest.mark.label_mapper
def test_pseudo_label_mapper(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    labels = 10
    elements = 50

    test_map = esets._pseudo_label_mapper(labels, elements)

    assert all(np.diff(test_map) != 0)
    assert len(test_map) == labels * elements


@pytest.mark.rises
def test_pseudo_label_mapper_raises(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    with pytest.raises(TypeError):
        esets._pseudo_label_mapper('10', '50')


@pytest.mark.label_mapper
def test_pure_label_mapper(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    labels = 10
    elements = 50

    test_map = esets._pure_label_mapper(labels, elements)

    assert all(np.diff(test_map) != 0)
    assert len(test_map) == labels * elements


@pytest.mark.rises
def test_pseudo_label_mapper_raises(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    with pytest.raises(TypeError):
        esets._pure_label_mapper('10', '50')


def test_within_category_random_map(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    test_labels = esets._pseudo_label_mapper(6, 12)
    test_map = esets._within_category_random_map(test_labels)

    assert len(np.unique(test_map)) == len(test_map)


def test_file_indexer(setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets

    # Test
    file_list = [file for file in sorted(os.listdir(esets.root_path))
                 if 'subsets' not in file and 'prerands' not in file]

    test_index = esets._file_indexer(categories, file_list)

    assert len(test_index) == len(file_list)


@pytest.mark.smoke
@pytest.mark.parametrize('method', ['pseudo_con', 'pure_con', 'unconstrained'])
def test_create_prerandomizations_from_subsets(method, setup_exprerands_from_subsets):
    esets = setup_exprerands_from_subsets
    file_number = [file for file in sorted(os.listdir(esets.root_path))
                   if 'subsets' not in file and 'prerands' not in file]

    subset_number = len(os.listdir(esets.subsets_path))
    prerand_number = 4

    esets.create_prerands(prerand_number, categories, method)
    prerands = sorted(os.listdir(esets.out_dir))

    assert len(prerands) == prerand_number * subset_number

    for file in prerands:
        path = os.path.join(esets.out_dir, file)
        prerand_df = pd.read_table(path, header=None)

        assert len(prerand_df) == file_number // subset_number


@pytest.mark.smoke
@pytest.mark.parametrize('method', ['pseudo_con', 'pure_con', 'unconstrained'])
def test_create_prerandomizations_from_expstim(method, setup_exprerands_from_expstim):
    esets = setup_exprerands_from_expstim
    file_list = [file for file in sorted(os.listdir(esets.root_path))
                   if 'subsets' not in file and 'prerands' not in file]

    prerand_number = 4

    esets.create_prerands(prerand_number, categories, method)
    prerands = sorted(os.listdir(esets.out_dir))

    assert len(prerands) == prerand_number

    for file in prerands:
        path = os.path.join(esets.out_dir, file)

        if method == 'unconstrained':
            prerand_df = pd.read_table(path)
        else:
            prerand_df = pd.read_table(path, header=None)

        assert len(prerand_df) == len(file_list)
