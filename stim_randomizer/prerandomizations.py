"""
Functions to create prerandomizations of your stimuli.

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import os

import numpy as np
import pandas as pd

from random import sample, choices


def file_indexer(cat_list, file_list):
    """Create a dictionary with keys ranging from 0 to len(file_list), which contains the name
    of the files together with their corresponding category.

    Parameters
    ----------
    cat_list: list
              contains keys corresponding to an integer for each category, and values
              with the name of said category

    file_list: list
               names of the files in strings

    Returns
    -------
    file_index: dict
                keys are numbers ranging from 0, and values are two-element tuples containing the
                filename as first value and its corresponding category as second value
    """

    # Determine the number of elements per category
    num_files = len(file_list)
    num_cat = len(cat_list)

    stim_per_cat = int(num_files / num_cat)

    # Create the index
    file_index = {key: (file_list[key], cat_list[cat]) for cat in range(num_cat)
                  for key in range(cat * stim_per_cat, (cat + 1) * stim_per_cat)}

    return file_index


def within_category_random_map(label_array):
    """Create array of range(len(label_array)), composed by numbers from 0 to len(label_array).

    The resulting list will preserve the category order of the input, but randomizing within each category.
    For example, if label_array were to have 10 elements of value 0 and 10 elements of value 1,
    a random permutation of numbers from 0 to 10 would be assigned where label_array == 0, and a
    random permutation of numbers from 11 to 20 where label_array == 1

    This function is intended to work with a previously randomized label_array for event designs, but it also
    can be used on a non-randomized array to ensure different pseudorandomizations of blocks in blocked designs.

    Parameters
    ----------
    label_array: np.array
                 array of numbers corresponding to different categories

    Returns
    -------
    output_list: list
                 a list containing a random permutation of numbers corresponding to each value of label_array.
    """

    # Initialize the output list.
    output_list = np.zeros(len(label_array))

    # Find out the number of categories...
    cat_num = len(np.unique(label_array))

    # ...and the number of elements for each category.
    stim_per_cat = int(len(label_array) / cat_num)

    for category in range(cat_num):

        output_list[label_array == category] = np.random.permutation(range(category * stim_per_cat, (category + 1) *
                                                                           stim_per_cat))

    output_list = output_list.astype(int)

    return output_list


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
                 randomized array of len(range(labels)) * elements) of numbers where no two consecutive elements are
                 the same value
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


def send_back(value, times, lst):
    """Helper function of pure_label_mapper. Inserts the value given at input in a position where the previous and
    next values are not the same.

    Note that the function performs the insertions in place, and does not return a new list.
    
    Parameters
    ----------
    
    value: int
           number that is going to be inserted on the list
           
    times: int
           number of times to insert the designated value

    lst: list
         input list where the values are going to be inserted

    Returns
    -------

    None
    """

    idx = len(lst)-2

    for _ in range(times):

        while lst[idx] == value or lst[idx-1] == value:

            idx -= 1

        lst.insert(idx, value)


def pure_label_mapper(labels, elements):
    """Array of len(labels) * elements length, randomly mapped so two consecutive elements are never of the same
    category (same number).

    The elements of the array will be generated one by one, picking from a population of the possible values, using
    weights to control the frequency. At each iteration, the selected element's weight will be set to 0 for the next
    iteration, and this value will be subtracted 1. In the end, there will be an equal number of each one of the
    population's values.

    The helper function send_back will take care of cases where the only values remaining are already the same as the
    one chosen by the last iteration (i.e., the population is empty).

    Parameters
    ----------
    labels: int
            desired number of categories

    elements: int
              number of stimuli per category

    Returns
    -------
    label_array: np.array
                 randomized array of len(range(labels)) * elements) of numbers where no two consecutive elements are
                 the same value
    """

    population = list(range(labels))

    weights = [elements] * labels
    label_list = []
    prev = None

    for i in range(labels * elements):

        if prev is not None:

            # Store the previous value and set its weight to 0 for the next iteration
            old_weight = weights[prev]
            weights[prev] = 0

        try:

            chosen = choices(population, weights)[0]

        except IndexError:

            # If all the weights are 0, the helper function will put the remaining values where
            # they do not violate the repetition constrain
            send_back(prev, old_weight, label_list)

            break

        label_list.append(chosen)
        weights[chosen] -= 1

        if prev is not None:

            # Restore weight
            weights[prev] = old_weight

        prev = chosen

    label_array = np.array(label_list)

    return label_array


def subset_parser(subsets_path):
    """Parses the .tsv files at the input directory and put the filenames into lists to be used for prerandomizations

    Parameters
    ----------

    subsets_path: str
                  directory containing tsv files with the filenames used in each subset

    Returns
    -------

    parsed_files: list
                  each element of the list is a sublist containing all the filenames of a given subset

    """

    parsed_files = []

    subsets = sorted(os.listdir(subsets_path))

    for subset in subsets:

        subset_path = os.path.join(subsets_path, subset)

        stim = pd.read_table(subset_path, header=None)

        stim_list = list(stim[0])

        parsed_files.append(stim_list)

    return parsed_files


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
            Note that, regardless of the option chosen, none of them will be executed if constrained is set to
            False.

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

    if subsets is True:

        all_stim = subset_parser(input_path)

    else:

        all_stim = [sorted(os.listdir(input_path))]

    if output_path == 'default':

        output_path = os.path.join(input_path, '../prerandomizations')

        if not os.path.exists(output_path):

            os.mkdir(output_path)

    for subset_num, subset in enumerate(all_stim):

        for prerand_num in range(prerandom_number):

            # Check for categories
            if categories is None or not constrained:

                # Shuffle the stim
                final_list = sample(subset, len(subset))

            # If there are categories, generate a label array depending on the chosen method
            else:

                cat_num = len(categories)
                files_per_cat = int(len(subset) / cat_num)

                if method == 'pseudo':

                    label_map = pseudo_label_mapper(cat_num, files_per_cat)

                elif method == 'pure':

                    label_map = pure_label_mapper(cat_num, files_per_cat)

                within_cat_map = within_category_random_map(label_map)

                file_index = file_indexer(categories, subset)

                final_list = [file_index[number] for number in within_cat_map]

            # Save it on a csv file
            if subsets is True:

                prerand_path = os.path.join(output_path,
                                            'set_' + str(subset_num + 1) + 'prerand_' + str(prerand_num + 1) + '.tsv')

            else:

                prerand_path = os.path.join(output_path,
                                            'prerand_' + str(prerand_num + 1) + '.tsv')

            with open(prerand_path, 'w') as csvfile:

                prerandwriter = csv.writer(csvfile)

                for stim in final_list:
                    prerandwriter.writerow([stim])
