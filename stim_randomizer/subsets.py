"""
Functions to create subsets of your stimuli.

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""
import csv
import os

from random import shuffle


def create_stim_sets(input_path, set_num, categories, output_path='default'):

    """Divide a list of files (stim) in n separated sets of equal length, with the same number
    of elements of each category in each set.

    The function will create a tsv file for each set, and save them at output_path.

    Parameters
    ----------

    input_path: str
               path to the folder containing the stim files, relative or absolute

    output_path: str
                desired path for the output files, relative or absolute

    set_num: int
             desired number of sets

    categories: tuple
                contains the names of the categories (as strings)

    Returns
    ------

    None
    """

    # Set the default output_path:

    if output_path == 'default':

        output_path = os.path.join(input_path, '../subsets')

    # Get a list of all the filenames, as well as the number of files per set (both total and for each category)
    total_stim = sorted(os.listdir(input_path))

    files_per_set = len(total_stim) // set_num
    files_per_cat_per_set = files_per_set // len(categories)

    # Initialize the sets
    subsets = {"set_" + str(_ + 1): [] for _ in range(set_num)}

    # For each category
    for category in categories:

        # ...get the files...
        cat_files = [file for file in total_stim if category in file]

        # ...shuffle them...
        shuffle(cat_files)

        # ...divide in as many chunks as sets...
        cat_chunks = [cat_files[n: n + files_per_cat_per_set] for n in range(0, len(cat_files), files_per_cat_per_set)]

        # ...and assign each chunk to a set.

        for _, subset in enumerate(subsets.keys()):

            subsets[subset].extend(cat_chunks[_])

    # Save the subsets in files
    for subset in subsets.keys():

        subsets_path = os.path.join(output_path, subset + '.tsv')

        with open(subsets_path, 'w') as csvfile:

            subsetwriter = csv.writer(csvfile)

            for stim in subsets[subset]:
                subsetwriter.writerow([stim])
