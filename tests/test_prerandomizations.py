"""
Tests for subsets.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import numpy as np
import os
import shutil
import tempfile

from stim_randomizer.prerandomizations import create_prerandomizations, pseudo_label_mapper, pure_label_mapper, within_category_random_map, file_indexer

# Define the categories
categories = ["human", "animal", "nature"]


def test_file_indexer():

    # Parameters
    files_per_category = 30

    # Create dummy input folder and files
    temp_input_folder = tempfile.mkdtemp()

    for category in categories:
        for _ in range(files_per_category):
            tempfile.mkstemp(prefix=(category + '%02d' % _), dir=temp_input_folder)

    file_list = sorted(os.listdir(temp_input_folder))

    test_index = file_indexer(categories, file_list)

    assert len(test_index) == len(file_list)

    # Delete temp folders and files
    shutil.rmtree(temp_input_folder)


def test_within_category_random_map():

    test_labels = pseudo_label_mapper(6, 12)
    test_map = within_category_random_map(test_labels)

    assert len(np.unique(test_map)) == len(test_map)


def test_pure_label_mapper():

    cat_num = 10
    elements = 50

    test_map = pure_label_mapper(cat_num, elements)

    assert np.sum(test_map[:-1] == test_map[1:]) == 0
    assert len(test_map) == cat_num * elements


def test_pseudo_label_mapper():

    cat_num = 10
    elements = 50

    test_map = pseudo_label_mapper(cat_num, elements)

    assert np.sum(test_map[:-1] == test_map[1:]) == 0
    assert len(test_map) == cat_num * elements


def test_create_prerandomizations():

    testing_parameters = {'file_number': [80, 90, 90],
                          'files_per_category': [0, 30, 30],
                          'prerandom_number': [3, 3, 3],
                          'constrained': [False, True, True],
                          'method': ['pseudo', 'pseudo', 'pure']}

    # From testing_parameters, create a list of dictionaries with the same keys, but only one of the values,
    # to use for the different test cases

    test_cases = [dict(zip(testing_parameters.keys(), case)) for case in zip(*testing_parameters.values())]

    for case in test_cases:

        # TEST CASE 1: 3 prerandomizations, no categories, no subsets
        # TEST CASE 2: 3 prerandomizations, 3 categories, no subsets, pseudo method
        # TEST CASE 3: 3 prerandomizations, 3 categories, no subsets, pure method

        # Create dummy input folder, output folder and files
        temp_input_folder = tempfile.mkdtemp()

        if case['files_per_category'] != 0:

            for category in categories:

                for i in range(case['files_per_category']):

                    tempfile.mkstemp(prefix=(category + '%02d' % i), dir=temp_input_folder)

        else:

            for file in range(case['file_number']):

                tempfile.mkstemp(dir=temp_input_folder)

        temp_output_folder = tempfile.mkdtemp()

        # Run the function and test
        create_prerandomizations(temp_input_folder,
                                 case['prerandom_number'],
                                 temp_output_folder,
                                 constrained=case['constrained'],
                                 method=case['method'])

        prerands = os.listdir(temp_output_folder)

        assert len(prerands) == case['prerandom_number']

        for file in prerands:

            path = os.path.join(temp_output_folder, file)

            with open(path, 'r') as prerand:

                assert sum(1 for row in prerand) == case['file_number']

        # Delete temp folders and files
        shutil.rmtree(temp_input_folder)
        shutil.rmtree(temp_output_folder)


test_create_prerandomizations()
test_pseudo_label_mapper()
test_pure_label_mapper()
test_within_category_random_map()
