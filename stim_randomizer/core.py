"""
Class to hold data of the experimental stimuli

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com

"""

import glob
import os


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
            self.categories = categories
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

        if len(categories) == len(all_files):
            categories = None

        return categories

    def request_subsets(self, set_number: int, dir_type: str = 'parent', check: bool = False):
        """
        Create an ExpSets() object and then calls create_subsets

        Parameters
        ----------

        set_number: int
                    desired number of sets

        check : bool, default: False
                if True, runs a checkup to make sure that is possible to create subsets of equal length
                and with the same number of categories per set

        dir_type: {'parent', 'child'}, default: parent
                  required parameter for the ExpSets class

        """
        self.subsets = ExpSets(self.path, dir_type)
        self.subsets.create_subsets(set_number, check)


class ExpSets:
    """
    The Expsets class will divide the stim in groups, and create
    csv files with the names of the files that are part of each set,
    so they can be easily loaded from the root folder by the experiment.

    Parameters
    ----------

    root_path: str
               absolute path to the directory that contains the stim files

    out_dir: {'parent', 'child'}
             'parent' will create a new 'subsets' dir at root_path's parent
             dir. 'child' will create the same new dir inside root_path
    """

    def __init__(self, root_path: str, out_dir: str):
        self.root_path = root_path
        self.out_dir = out_dir

    def create_subsets(self, set_num, check):
        pass
