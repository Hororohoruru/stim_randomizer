"""
Functions to create subsets of your stimuli.

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""
import os

from random import shuffle


def create_stim_sets(input_path, output_path, set_num, categories):

    """Divide a list of files (stim) in n separated sets of equal length, with the same number
    of elements of each category in each set

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

    output_set: csv file
                file containing the names of the stim for a given set. Note that there will be n files, being n
                the variable set_num"""

    # Get a list of all the filenames, as well as the number of files per set (both total and for each category)
    total_stim = sorted(os.listdir(input_path))

    files_per_set = len(total_stim) / set_num
    files_per_cat_per_set = files_per_set / len(categories)

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

            subsets[subset].append(cat_chunks[_])