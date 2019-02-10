"""
Tests for the ExpStim class inside core.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

from stim_randomizer.core import ExpStim


categories = ['animal', 'human', 'nature']


def test_instance_with_categories_assigns_categories_correctly(setup_expstim_cat):
    """test that ExpStim.categories are correctly set up"""

    # GIVEN an instance of ExpStim (providing and not providing explicit categories)
    # THEN in both cases the returned categories should be correcly assigned

    es = setup_expstim_cat

    assert sorted(es.categories) == sorted(categories)


def test_path_is_assigned_correctly(setup_cat_dir):
    tmpdir = str(setup_cat_dir)
    es = ExpStim(tmpdir)

    assert es.path == tmpdir


def test_scan_categories_finds_categories(setup_expstim_cat):
    es = setup_expstim_cat

    assert sorted(es._scan_categories()) == sorted(categories)


def test_scan_categories_assigns_none_when_no_categories(setup_expstim_plain):
    es = setup_expstim_plain

    assert es._scan_categories() is None


def test_instance_without_categories_assigns_correct_attribute(setup_expstim_plain):
    es = setup_expstim_plain

    assert es.categories is None


def test_request_subsets_creates_expsets_instance(setup_expstim_cat):

    experiment = setup_expstim_cat
    experiment.request_subsets(15)

    # assert isinstance(experiment.subsets, ExpSets)


def test_request_subsets_creates_subsets(setup_expstim_cat, mocker):

    mock_subset = mocker.patch('stim_randomizer.core.ExpSets')
    experiment = setup_expstim_cat

    experiment.request_subsets(15)

    mock_subset.return_value.create_subsets.assert_called_with(15, False)
    mock_subset.return_value.create_subsets.assert_called_once()


