"""
Functions to create prerandomizations of your stimuli.

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import os

from random import shuffle


def create_prerandomizations(input_path, prerandom_number, output_path='default', categories=None, subsets=None,
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

    subsets: int, default None
             number of subsets, if any. In case a value is provided, the prerandomization will look for files
             named up to 'subset_[subsets].tsv'. At default value, it assumes the directory provided in input_path
             contains the stim files.

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
