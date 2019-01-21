"""
Tests for prerandomizations.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import json
import os
import pytest
import shutil
import tempfile

import numpy as np
import pandas as pd

from pprint import pprint

from stim_randomizer.prerandomizations import create_prerandomizations, _pseudo_label_mapper, _pure_label_mapper, \
    _within_category_random_map, _file_indexer, _subset_parser

from stim_randomizer.subsets import create_stim_sets


@pytest.fixture(scope='session')
def init_params():

    with open('prerandom_test_params.json', 'r') as config:
        prerand_params = json.load(config)

    return prerand_params

# # Initialize parameters
#
# with open('prerandom_test_params.json', 'r') as config:
#     prerand_params = json.load(config)
#
# categories = prerand_params['categories']
# cases_parameters = prerand_params['cases_parameters']


def cleanup_files(*args):
    """Delete all the folders given as input, and the files inside them

    Parameters
    ----------

    *args: tuple
           directories you want to remove
    """

    for path in args:
        shutil.rmtree(path)


def set_up_subsets(file_number, set_number, cat_list):
    """Perform setup for tests that need subsets as an input

    Parameters
    ----------

    file_number: int
                 total number of files from which subsets will be created

    set_number: int
                number of subsets desired

    cat_list: tuple
              categories that will be used to create the files

    Returns
    -------

    subset_folder: str
                   path which contains the .tsv files for the subsets

    output_folder: str
                   path for the output of the test functions
    """

    temp_input_folder = tempfile.mkdtemp()
    subset_folder = tempfile.mkdtemp()
    output_folder = tempfile.mkdtemp()

    for category in cat_list:
        for _ in range(file_number // len(cat_list)):
            tempfile.mkstemp(prefix=(category + '%02d' % _), dir=temp_input_folder)

    create_stim_sets(temp_input_folder, set_number, cat_list, output_path=subset_folder)

    shutil.rmtree(temp_input_folder)

    return subset_folder, output_folder


def set_up_files(file_number, cat=False, categories=None):
    """Performs the necessary setup for test functions that take files as input

    Parameters
    ----------

    file_number: int
                 number of files that will be created as input. If cat is False, this will be the total number of
                 files. If it is set to True, this will be the number of files per category

    cat: bool, default False
         if True, it will append the category names provided in categories to the temp files

    categories: tuple, default None
                names of the categories to be used. Note that it will only be taken into account if cat=True

    Returns
    -------

    input_folder: str
                  path to the temporary input folder, containing the files to be used by the tests

    output_folder: str
                   path to the output folder, where the files created by the functions will be
    """

    input_folder = tempfile.mkdtemp()
    output_folder = tempfile.mkdtemp()

    if cat:
        for category in categories:
            for i in range(file_number):
                tempfile.mkstemp(prefix=(category + '%02d' % i), dir=input_folder)

    else:
        for file in range(file_number):
            tempfile.mkstemp(dir=input_folder)

    return input_folder, output_folder


# @pytest.fixture()
# def setup_test():
#     """Setup-teardown fixture test"""
#
#     temp_input_folder, _ = set_up_files(30, cat=True, categories=categories)
#
#     yield
#
#     cleanup_files(temp_input_folder)

# @pytest.mark.fixtures()
def test_file_indexer(init_params):

    # Parameters
    files_per_category = 30
    categories = init_params['categories']

    # Create dummy input folder and files
    temp_input_folder, _ = set_up_files(files_per_category, cat=True, categories=categories)

    # Test
    file_list = sorted(os.listdir(temp_input_folder))
    test_index = _file_indexer(categories, file_list)

    assert len(test_index) == len(file_list)

    cleanup_files(temp_input_folder)


def test_within_category_random_map():

    test_labels = _pseudo_label_mapper(6, 12)
    test_map = _within_category_random_map(test_labels)

    assert len(np.unique(test_map)) == len(test_map)


def test_pure_label_mapper():

    cat_num = 10
    elements = 50

    test_map = _pure_label_mapper(cat_num, elements)

    assert np.sum(test_map[:-1] == test_map[1:]) == 0
    assert len(test_map) == cat_num * elements


@pytest.mark.rises
def test_pure_label_mapper_raises():

    with pytest.raises(TypeError):
        _pure_label_mapper('10', '50')


def test_pseudo_label_mapper():

    cat_num = 10
    elements = 50

    test_map = _pseudo_label_mapper(cat_num, elements)

    assert np.sum(test_map[:-1] == test_map[1:]) == 0
    assert len(test_map) == cat_num * elements


@pytest.mark.rises
def test_pseudo_label_mapper_raises():

    with pytest.raises(TypeError):
        _pseudo_label_mapper('10', '50')


def test_subset_parser(init_params):

    # Variables
    file_number = 144
    number_of_sets = 4
    files_per_set = file_number // number_of_sets
    categories = init_params['categories']

    subset_folder, _ = set_up_subsets(file_number, number_of_sets, categories)

    parsed_sets = _subset_parser(subset_folder)

    # Test

    assert len(parsed_sets) == len(os.listdir(subset_folder))

    for subset in parsed_sets:

        assert len(subset) == files_per_set

    cleanup_files(subset_folder, _)


# From testing_parameters, create a list of dictionaries with the same keys, but only one of the values,
# to use for the different test cases

# test_cases = [dict(zip(cases_parameters.keys(), case)) for case in zip(*cases_parameters.values())]
# cases_ids = [c["id"] for c in test_cases]


# @pytest.mark.smoke
# @pytest.mark.parametrize('case', init_params['test_cases'], ids=init_params['cases_ids'])
# def test_create_prerandomizations(case):
#
#     # TEST CASE 1: 3 prerandomizations, no categories, no subsets
#     # TEST CASE 2: 3 prerandomizations, 3 categories, no subsets, pseudo method
#     # TEST CASE 3: 3 prerandomizations, 3 categories, no subsets, pure method
#     # TEST CASE 4: 3 prerandomizations, 3 categories, 4 subsets, pseudo method
#
#     if case['subsets']:
#         temp_input_folder, temp_output_folder = set_up_subsets(case['file_number'],
#                                                                case['subset_number'],
#                                                                case['categories'])
#
#     elif case['files_per_category'] != 0:
#         temp_input_folder, temp_output_folder = set_up_files(case['files_per_category'],
#                                                              cat=True,
#                                                              categories=case['categories'])
#
#     else:
#         temp_input_folder, temp_output_folder = set_up_files(case['file_number'])
#
#     # Run the function and test
#     create_prerandomizations(temp_input_folder,
#                              case['prerandom_number'],
#                              temp_output_folder,
#                              categories=case['categories'],
#                              subsets=case['subsets'],
#                              constrained=case['constrained'],
#                              method=case['method'])
#
#     prerands = os.listdir(temp_output_folder)
#     pprint(sorted(os.listdir(temp_output_folder)))
#
#     assert len(prerands) == case['prerandom_number'] * case['subset_number']
#
#     for file in prerands:
#         path = os.path.join(temp_output_folder, file)
#         prerand_df = pd.read_table(path, header=None)
#
#         if case['subsets']:
#             assert len(prerand_df) == case['file_number'] // case['subset_number']
#         else:
#             assert len(prerand_df) == case['file_number']
#
#     # Delete temp folders and files
#     cleanup_files(temp_input_folder, temp_output_folder)


@pytest.mark.rises
def test_create_prerandomizations_raises(init_params):

    temp_input_folder, temp_output_folder = set_up_files(30,
                                                         cat=True,
                                                         categories=init_params['categories'])

    with pytest.raises(ValueError) as excinfo:

        create_prerandomizations(temp_input_folder,
                                 3,
                                 temp_output_folder,
                                 categories=init_params['categories'],
                                 subsets=False,
                                 constrained=True,
                                 method='mocos')

        exception_msg = excinfo.value.args[0]

        assert exception_msg == "method argument must be 'pseudo' or 'pure'"

        # Delete temp folders and files
        cleanup_files(temp_input_folder, temp_output_folder)
