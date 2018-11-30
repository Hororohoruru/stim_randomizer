"""
Tests for subsets.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import os
import shutil
import tempfile

from stim_randomizer.prerandomizations import create_prerandomizations


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