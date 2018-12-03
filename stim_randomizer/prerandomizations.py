"""
Functions to create prerandomizations of your stimuli.

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import numpy as np
import os

from random import shuffle


def pseudo_label_mapper(labels, elements):
    """Array of len(labels) * elements length, randomly mapped so two consecutive elements are never of the same
    category (same number).

    Chunks containing one number per category will be randomized and inserted on the final list. At each iteration,
    the function will check if the first element of the current chunk is the same as the last element of the previous
    one. If this is the case, the first element of the current chunk will be swapped with the last one.

    This function assumes that the set has the same number of elements for each category.

    Parameters
    ----------
    labels: int
            desired number of categories

    elements: int
              number of stimuli per category

    Returns
    -------
    label_array: np.array
                 randomized array of len(range(labels)) * elements) of numbers where
    """

    for blocks in range(0, elements):

        chunk = np.arange(labels)
        np.random.shuffle(chunk)

        try:
            if chunk[0] == label_list[-1]:
                chunk[0], chunk[-1] = chunk[-1], chunk[0]
        except NameError:
            label_list = []

        label_list.extend(chunk)

    label_array = np.array(label_list)

    return label_array


def create_prerandomizations(input_path, prerandom_number, output_path='default', categories=None, subsets=False,
                             constrained=False, method='pseudo'):

    """Generate a number of random orders for previously existing stim files, and save each of them to a
    csv file to be loaded later by your experiment

    Parameters
    ----------

    input_path: str
                directory containing the files. If the files have been divided into subsets, this parameter
                will look for subset files at this directory and work with each of the subsets

    prerandom_number: int
                      desired number of prerandomizations. If subsets exist, this will be the number of
                      prerandomizations created for each subset

    output_path: str, default 'default'
                 directory where the prerandomization files will be stored. If it is not provided, it defaults
                 to ...[input_path]/../prerandomizations

    categories: list, default None
                if the stimuli is divided into categories, a list containing them as strings should be provided
                here

    subsets: bool, default False
             variable denoting the existence of subsets. If True, the function will treat the elements of the input
             directory as .tsv files containing the stim of each subset. At default value, it assumes the directory
             provided in input_path contains the stim files.

    constrained: bool, default False
                 if set to True, the prerandomizations will follow the constrain that two consecutive elements are
                 never of the same category. Note that this parameter can only be used if categories is not None

    method: str, default 'pseudo'
            method of choice for the constrained prerandomizations. The availeble options are: 'pseudo', 'pure'.

            The 'pseudo' method will generate the order by creating a sublist with one element of each category,
            shuffle said elements, and append it to the final list. At each step, it will check that the first
            element of the new sublist is not the same category as the last one of the previously appended one.
            If that were the case, the first element will be swapped with the last one, and then appended to the
            final list. Although this is not a true randomization, it ensures that the different category will
            be more homogeneously distributed during the run, which can be desirable for certain experiments.
            Is is handled by the constrained_pseudo_shuffle function.

            The 'pure' method will generate each element of the list one by one, taking each one from a population
            of possible values and setting the chances of taking the same value to 0 for the next iteration. If at
            the end of the process, only values equal to the previously inserted one remain, a helper function will
            look back for places on the list where inserting the remaining values would not violate the constrain.
            It is handled by the constrained_pure_shuffle function.
    """

    all_stim = sorted(os.listdir(input_path))

    for prerand_num in prerandom_number:

        # Check for categories
        if categories is None or not constrained:

            # Shuffle the stim
            shuffle_stim = shuffle(all_stim)

            # Save it on a csv file
            prerand_path = os.path.join(output_path, 'prerand_' + str(prerand_num))

            with open(prerand_path, 'w') as csvfile:

                prerandwriter = csv.writer(csvfile, delimiter='\t')
                prerandwriter.writerow(shuffle_stim)

        elif method == 'pseudo':

            cat_num = len(categories)
            files_per_cat = len(all_stim) / cat_num

            shuffle_stim = pseudo_label_mapper(cat_num, files_per_cat)

        elif method == 'pure':

            pass