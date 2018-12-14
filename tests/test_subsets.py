"""
Tests for subsets.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import json
import os
import pytest
import shutil
import tempfile

import pandas as pd

from stim_randomizer.subsets import create_stim_sets

with open('test_subsets.json', 'r') as data:
    params = json.load(data)


def test_create_stim_sets():

    # Define the categories
    categories = params["categories"]

    # Variables
    files_per_category = params["files_per_category"]
    number_of_sets = params["number_of_sets"]
    files_per_set = files_per_category * len(categories) / number_of_sets

    # Create dummy input folder and files
    temp_input_folder = tempfile.mkdtemp()

    for category in categories:
        for _ in range(files_per_category):
            tempfile.mkstemp(prefix=(category + '%02d' % _), dir=temp_input_folder)

    # Create dummy output folder
    temp_output_folder = tempfile.mkdtemp()

    # Test stuff
    create_stim_sets(temp_input_folder, number_of_sets, categories, output_path=temp_output_folder)

    subsets = sorted(os.listdir(temp_output_folder))

    assert len(subsets) == number_of_sets

    for subset in subsets:

        subset_path = os.path.join(temp_output_folder, subset)

        subset_df = pd.read_table(subset_path, header=None)

        assert files_per_set == len(subset_df)

        for category in categories:

            assert len(subset_df[subset_df[0].str.contains(category)]) == files_per_set // len(categories)

    shutil.rmtree(temp_input_folder)
    shutil.rmtree(temp_output_folder)

