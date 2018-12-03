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

from stim_randomizer.prerandomizations import create_prerandomizations, pseudo_label_mapper


def test_pseudo_label_mapper():

    cat_num = 10
    elements = 50

    test_map = pseudo_label_mapper(cat_num, elements)

    assert np.sum(test_map[:-1] == test_map[1:]) == 0
    assert len(test_map) == cat_num * elements


def test_create_prerandomizations():

    # Define the categories
    categories = ["human", "animal", "nature"]

    # TEST CASE 1: 3 prerandomizations, no categories, no subsets

    # Parameters
    file_number = 80
    prerandom_number = 3

    # Create dummy input folder and files
    temp_input_folder = tempfile.mkdtemp()

    for file in range(file_number):
        tempfile.mkstemp(dir=temp_input_folder)

    # Run the function and test
    create_prerandomizations(temp_input_folder, prerandom_number)

    temp_output_folder = os.path.join(temp_input_folder, '../prerandomizations')

    prerands = os.listdir(temp_output_folder)

    assert len(prerands) == prerandom_number

    for file in prerands:
        with csv.reader(file) as prerand:

            assert sum(1 for row in file) == file_number

    # Delete temp folders and files
    shutil.rmtree(temp_input_folder)
    shutil.rmtree(temp_output_folder)

    # TEST CASE 2: 3 prerandomizations, 3 categories, no subsets, pseudo method

    # Parameters
    files_per_category = 30
    prerandom_number = 3
    file_number = files_per_category * len(categories)

    # Create dummy input folder and files
    temp_input_folder = tempfile.mkdtemp()

    for category in categories:
        for _ in range(files_per_category):
            tempfile.mkstemp(prefix=(category + '%02d' % _), dir=temp_input_folder)

    # Run the function and test
    create_prerandomizations(temp_input_folder, prerandom_number)

    temp_output_folder = os.path.join(temp_input_folder, '../prerandomizations')

    prerands = os.listdir(temp_output_folder)

    assert len(prerands) == prerandom_number

    for file in prerands:
        with csv.reader(file) as prerand:

            assert sum(1 for row in file) == file_number

    # Delete temp folders and files
    shutil.rmtree(temp_input_folder)
    shutil.rmtree(temp_output_folder)