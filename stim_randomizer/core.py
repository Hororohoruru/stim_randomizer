"""
Class to hold data of the experimental stimuli

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import csv
import glob
import os

from random import shuffle


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

        pass
