"""
Functions to create subsets of your stimuli.

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

from random import shuffle


def create_sets(input_url, output_url, set_num, *categories):

    """Divide a list of files (stim) in n separated sets of equal length, with the same number
    of elements of each category in each set

    Parameters
    ----------

    input_url: str
               path to the folder containing the stim files, relative or absolute

    output_url: str
                desired path for the output files, relative or absolute

    set_num: int
             desired number of sets

    *categories: list
                 contains the names of the categories (as strings)

    Output
    ------

    output_set: csv file
                file containing the names of the stim for a given set. Note that there will be n files, being n
                the variable set_num"""