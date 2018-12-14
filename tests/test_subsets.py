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

with open('subsets_test_params.json', 'r') as data:
    prerand_params = json.load(data)

categories = prerand_params['categories']
cases_parameters = prerand_params['cases_parameters']

# From testing_parameters, create a list of dictionaries with the same keys, but only one of the values,
# to use for the different test cases
test_cases = [dict(zip(cases_parameters.keys(), case)) for case in zip(*cases_parameters.values())]


@pytest.mark.parametrize('case', test_cases)
def test_create_stim_sets(case):

    # Variables
    files_per_category = case["files_per_category"]
    number_of_sets = case["number_of_sets"]
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

            assert len(subset_df[subset_df[0].str.contains(category)]) == files_per_set / len(categories)

    shutil.rmtree(temp_input_folder)
    shutil.rmtree(temp_output_folder)

