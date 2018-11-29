"""
Tests for subsets.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import glob
import os
import shutil
import tempfile

from stim_randomizer.subsets import create_stim_sets

path = os.getcwd()

def test_create_stim_sets():


    # Define the categories
    categories = ('animal', 'human', 'nature')

    # Variables
    files_per_category = 48
    number_of_sets = 4
    files_per_set = files_per_category * len(categories) / number_of_sets

    # Create dummy input folder and files
    temp_input_folder = tempfile.mkdtemp()

    for category in categories:
        for _ in range(files_per_category):
            tempfile.mkstemp(prefix=(category + '%02d' % _), dir=temp_input_folder)

    # Create dummy output folder
    temp_output_folder = tempfile.mkdtemp()

    # Test stuff
    create_stim_sets(temp_input_folder, temp_output_folder, number_of_sets, categories)

    subsets = os.listdir(temp_output_folder)

    assert len(subsets) == number_of_sets

    for subset in subsets:
        with csv.reader(subset) as file:
            assert files_per_set == sum(1 for row in file)

            for category in categories:
                assert len(glob.glob('*' + category + '*')) == files_per_set / len(categories)

    shutil.rmtree(temp_input_folder)
    shutil.rmtree(temp_output_folder)