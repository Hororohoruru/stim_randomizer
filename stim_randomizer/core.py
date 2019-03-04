"""
Class to hold data of the experimental stimuli

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import glob
import os

import numpy as np
import pandas as pd

from random import shuffle, choices


class ExpStim:
    """
    The ExpStim object contains info about the stimuli, and will pass this info to the SubSets and PreRand
    objects to request the creation of subsets and prerandomizations of said stimuli

    Parameters
    ----------

    path: str
          assign directory attribute

    categories: list of str, default: None
                list with the names of the categories in the stim. It defaults to None

    Attributes
    ----------

    path: str
          absolute path containing the stimuli

    categories: list
                names of the categories of the files. The object will look for category names on the given path
                upon instantiation if not provided. If it doesn't find any, it will be set to None

    subsets: ExpSets object
             wrapper for subset information. It is initialized as None until creation is requested

    prerands: ExpRands object
              wrapper for subset information. It is initialized as None until creation is requested


    """

    def __init__(self, path: str, categories: list or None = None) -> None:

        self.subsets = None
        self.prerands = None
        self.path = path

        if categories:
            self.categories = sorted(categories)
        else:
            self.categories = self._scan_categories()

    def _scan_categories(self) -> list or None:
        """
        Looks for categories in self.path and returns a list with the categories found, or None if it does not find
        any

        Returns
        -------

        categories: list of str
                    list containing the names of the categories, provided that the files are named in a
                    "[category]_[number]" fashion
        """

        all_files = os.listdir(self.path)

        categories = list(set([file.split("_")[0] for file in all_files]))

        if len(categories) == len(all_files) or len(categories) > (len(all_files) // 2):
            categories = None

        return categories

    def request_subsets(self, set_number: int, dir_type: str = 'parent') -> None:
        """
        Create an ExpSets() object and then calls create_subsets

        Parameters
        ----------

        set_number: int
                    desired number of sets

        dir_type: {'parent', 'child'}, default: parent
                  required parameter for the ExpSets class

        Returns
        -------

        None
        """

        self.subsets = ExpSets(self.path, dir_type)
        self.subsets.create_subsets(set_number, self.categories)

    def request_prerands(self, prerand_number: int, method: str = 'pseudo_con', dir_type: str = 'parent') -> None:
        """
        Create an ExPrerands() object and call create_prerands

        Parameters
        ----------

        prerand_number: int
                        desired number of prerands

        method: {'unconstrained', 'pseudo_con', 'pure_con'}
                required parameter for the ExPrerands class

        dir_type: {'parent', 'child'}, default: parent
                  required parameter for the ExpSets class

        Returns
        -------

        None
        """

        if self.subsets:
            self.prerands = ExPrerands(self.path, self.subsets.out_dir, dir_type)
        else:
            self.prerands = ExPrerands(self.path, self.subsets, dir_type)

        self.prerands.create_prerands(prerand_number, self.categories, method)


class ExpSets:
    """
    The Expsets class will divide the stim in groups, and create
    csv files with the names of the files that are part of each set,
    so they can be easily loaded from the root folder by the experiment.

    Parameters
    ----------

    root_path: str
               absolute path to the directory that contains the stim files

    dir_type: {'parent', 'child'}
              handles where to create the output directory with the helper
              method _get_dir

    Attributes
    ----------

    root_path: str
               absolute path to the stim files

    dir_type: {'parent', 'child'}
              type of out_dir generation

    out_dir: str
             absolute path to the files containing the subset info
    """

    def __init__(self, root_path: str, dir_type: str) -> None:
        self.root_path = root_path
        self.dir_type = dir_type
        self.out_dir = self._get_dir(self.dir_type)

    def _get_dir(self, dir_type: str) -> str:
        """
        Check desired dir_type and create out_dir where requested

        Parameters
        ----------

        dir_type: {'parent', 'child'}
                  'parent' creates the 'subsets' folder in the parent dir
                  of the root dir, and 'child' creates it inside the root dir

        Returns
        -------

        out_dir: str
                 absolute path of the output directory
        """

        if dir_type == 'parent':
            out_dir = os.path.join(self.root_path,
                                   '../subsets')
        elif dir_type == 'child':
            out_dir = os.path.join(self.root_path,
                                   'subsets')
        else:
            raise ValueError('dir_type must be either "parent" or "child"')

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        return out_dir

    def create_subsets(self, set_num: int, categories: list or None) -> None:
        """
        Method to create subsets. The subsets will be csv files containing
        names of the files from self.root_path. Each subset will contain the
        same number of files and the same number of files per category. If
        this is not possible, an exception will be thrown and the function
        will stop.

        Parameters
        ----------

        set_num: int
                 desired number of sets

        categories: list or None
                    names of the categories passed from the ExpStim class,
                    if any

        Returns
        -------

        None
        """

        total_stim = sorted([file for file in os.listdir(self.root_path) if 'subsets' not in file])

        if len(total_stim) % set_num != 0:
            remaining_stim = len(total_stim) % set_num
            error_set_msg = ("It is not possible to equally divide '{0}' stim into '{1}' sets."
                             " '{2}' files would be remaining".format(total_stim, set_num, remaining_stim))

            raise ValueError(error_set_msg)

        files_per_set = len(total_stim) // set_num

        try:
            if files_per_set % len(categories) != 0:
                remaining_cat_stim = files_per_set % len(categories)
                error_cat_msg = ("It is not possible to divide the files and preserve the same number of categories "
                                 "per subset for '{0}' categories. '{1}' files would be "
                                 "remaining".format(set_num, remaining_cat_stim))

                raise ValueError(error_cat_msg)

        except TypeError as e:
            raise TypeError('The stim you are trying to divide has no categories') from e

        else:
            files_per_cat_per_set = files_per_set // len(categories)

        subsets = {"subset_" + str(i + 1): [] for i in range(set_num)}

        # For each category
        for category in categories:

            # ...get the files...
            cat_files = [file for file in total_stim if category in file]

            # ...shuffle them...
            shuffle(cat_files)

            # ...divide in as many chunks as sets...
            cat_chunks = [cat_files[n: n + files_per_cat_per_set] for n in
                          range(0, len(cat_files), files_per_cat_per_set)]

            # ...and assign each chunk to a set.

            for i, subset in enumerate(subsets.keys()):
                subsets[subset].extend(cat_chunks[i])

            # Save the subsets in files
            for subset in subsets.keys():

                subsets_path = os.path.join(self.out_dir, subset + '.tsv')

                with open(subsets_path, 'w') as csvfile:

                    subsetwriter = csv.writer(csvfile)

                    for stim in subsets[subset]:
                        subsetwriter.writerow([stim])


class ExPrerands:
    """
    The ExPrerands class will create constrained prerandomizations for the provided groups
    of stimuli, be them a whole list or different subsets saved in csv files. The output
    will be saved in csv files.

    Parameters
    ----------

    root_path: str
               absolute path to the directory that contains the stim files

    subsets_path: str or None
                  absolute path to the directory that contains the subset files

    dir_type: {'parent', 'child'}
              handles where to create the output directory with the helper
              method _get_dir

    Attributes
    ----------

    root_path: str
               absolute path to the stim files

    subsets_path: str or None
                  absolute path to the directory that contains the subset files

    dir_type: {'parent', 'child'}
              handles where to create the output directory with the helper
              method _get_dir

    out_dir: str
             absolute path to the files containing the prerand info
    """

    def __init__(self, root_path: str, subsets_path: str or None, dir_type: str) -> None:
        self.root_path = root_path
        self.subsets_path = subsets_path
        self.dir_type = dir_type
        self.out_dir = self._get_dir(self.dir_type)

    def _get_dir(self, dir_type: str) -> str:
        """
        Check desired dir_type and create out_dir where requested

        Parameters
        ----------

        dir_type: {'parent', 'child'}
                  'parent' creates the 'prerands' folder in the parent dir
                  of the root dir, and 'child' creates it inside the root dir

        Returns
        -------

        out_dir: str
                 absolute path of the output directory
        """

        if dir_type == 'parent':
            out_dir = os.path.join(self.root_path,
                                   '../prerands')
        elif dir_type == 'child':
            out_dir = os.path.join(self.root_path,
                                   'prerands')
        else:
            raise ValueError('dir_type must be either "parent" or "child"')

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        return out_dir

    @staticmethod
    def _subset_parser(subsets_path):
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

        # subsets = sorted(os.listdir(subsets_path))
        subsets = glob.glob(os.path.join(subsets_path, '*'))

        for subset in subsets:
            subset_path = os.path.join(subsets_path, subset)

            stim_df = pd.read_table(subset_path, header=None, engine='python')
            stim_list = [stim for stim in stim_df[0]]

            parsed_files.append(stim_list)

        return parsed_files

    @staticmethod
    def _pseudo_label_mapper(labels: int, elements: int) -> 'np.array':
        """
        Creates an array of len(labels) * elements length, randomly mapped so two consecutive
        elements are never of the same category (same number).

        Chunks containing one number per category will be randomized and inserted on the final list.
        At each iteration, the function will check if the first element of the current chunk is the
        same as the last element of the previous one. If this is the case, the first element of the
        current chunk will be swapped with the last one.

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

    @staticmethod
    def _send_back(value: int, times: int, lst: list) -> None:
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

        idx = len(lst) - 2

        for _ in range(times):
            while lst[idx] == value or lst[idx - 1] == value:
                idx -= 1

            lst.insert(idx, value)

    def _pure_label_mapper(self, labels: int, elements: int) -> 'np.array':
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
                self._send_back(prev, old_weight, label_list)
                break

            label_list.append(chosen)
            weights[chosen] -= 1

            if prev is not None:
                # Restore weight
                weights[prev] = old_weight

            prev = chosen

        label_array = np.array(label_list)

        return label_array

    def _get_label_mapper(self, method: str) -> 'function':
        """
        Getter for the function to create a label array depending on the method

        Parameters
        ----------

        method: {'pseudo_con', 'pure_con'}
                method for prerandomization of the categories

        Returns
        -------

        function: _pure_label_mapper or _pseudo_label_mapper
                  function in charge of creating the label array for the randomization
        """

        if method == 'pseudo_con':
            return self._pseudo_label_mapper

        elif method == 'pure_con':
            return self._pure_label_mapper

    def _label_mapper(self, categories: list, files: list, method: str) -> 'function':
        """
        Get parameters and call the correct label mapping function

        Parameters
        ----------

        categories: list
                    the length of the list will be used to create the labels for the label
                    mapper

        files: list
               the length will be used to know the necessary number for each label in the
               label mapper

        Returns
        -------

        label_mapper : function
                       call to the corresponding label mapping function with the correct parameters

        """

        labels = len(categories)
        elements = int(len(files) // labels)

        label_mapper = self._get_label_mapper(method)
        return label_mapper(labels, elements)

    @staticmethod
    def _within_category_random_map(label_array):
        """Create array of range(len(label_array)), composed by numbers from 0 to len(label_array).

        The resulting list will preserve the category order of the input, but randomizing within each category.
        For example, if label_array were to have 10 elements of value 0 and 10 elements of value 1,
        a random permutation of numbers from 0 to 10 would be assigned where label_array == 0, and a
        random permutation of numbers from 11 to 20 where label_array == 1

        This function is intended to work with a previously randomized label_array for event designs, but it also
        can be used on a non-randomized array to ensure different prerandomizations of blocks in blocked designs.

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
            output_list[label_array == category] = np.random.permutation(
                range(category * stim_per_cat, (category + 1) *
                      stim_per_cat))

        output_list = output_list.astype(int)

        return output_list

    @staticmethod
    def _file_indexer(cat_list, file_list):
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
        file_index = {key: file_list[key] for cat in range(num_cat)
                      for key in range(cat * stim_per_cat, (cat + 1) * stim_per_cat)}

        return file_index

    def create_prerands(self, prerand_num: int, categories: list or None, method: str) -> None:
        """
        Method to create prerandomizations. The subsets will be csv files containing
        names of the files from self.root_path or in self.subsets_path, depending on
        the existence of subsets. Each prerand will contain the same filenames, but
        in different randomized orders.

        Parameters
        ----------

        prerand_num: int
                     desired number of sets

        categories: list or None
                    names of the categories passed from the ExpStim class, if any

        method: {'unconstrained', 'pseudo_con', 'pure_con'}
                prerandomization method

        Returns
        -------

        None
        """

        if self.subsets_path:
            all_stim = self._subset_parser(self.subsets_path)
        else:
            all_stim = [sorted(os.listdir(self.root_path))]

        for subset_num, subset in enumerate(all_stim):
            for prerand in range(prerand_num):
                if not categories or method == 'unconstrained':
                    shuffle(subset)
                    final_list = subset

                else:
                    label_map = self._label_mapper(categories, subset, method)

                    try:
                        within_cat_map = self._within_category_random_map(label_map)
                    except UnboundLocalError as err:
                        raise ValueError("method argument must be 'pseudo_con' or 'pure_con'") from err

                    file_index = self._file_indexer(categories, subset)

                    final_list = [file_index[number] for number in within_cat_map]

                # Saving to files
                if self.subsets_path:
                    prerand_path = os.path.join(self.out_dir,
                                                'set_' + str(subset_num + 1) + 'prerand_' +
                                                str(prerand + 1) + '.tsv')
                else:
                    prerand_path = os.path.join(self.out_dir,
                                                'prerand_' + str(prerand + 1) + '.tsv')

                with open(prerand_path, 'w') as csvfile:
                    prerandwriter = csv.writer(csvfile)

                    for stim in final_list:
                        prerandwriter.writerow([stim])
