"""
Tests for the ExpStim class inside core.py

Author: Juan Jesus Torre Tresols
Mail: juanjesustorre@gmail.com
"""

import pdb
import pytest

from stim_randomizer.core import ExpStim, ExpSets, ExPrerands

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


@pytest.mark.subsets
def test_request_subsets_creates_expsets_instance(setup_expstim_cat):

    experiment = setup_expstim_cat
    experiment.request_subsets(10)

    assert isinstance(experiment.subsets, ExpSets)


@pytest.mark.subsets
def test_request_subsets_creates_subsets(setup_expstim_cat, mocker):

    mock_subset = mocker.patch('stim_randomizer.core.ExpSets')
    experiment = setup_expstim_cat

    experiment.request_subsets(10, sorted(categories))

    mock_subset.return_value.create_subsets.assert_called_with(10, sorted(categories))
    mock_subset.return_value.create_subsets.assert_called_once()


@pytest.mark.prerands
@pytest.mark.parametrize('method', ['unconstrained', 'pure_con', 'pseudo_con'])
def test_request_prerands_creates_exprerands_instance(setup_expstim_cat, method):

    experiment = setup_expstim_cat
    experiment.request_prerands(5, method)

    assert isinstance(experiment.prerands, ExPrerands)


@pytest.mark.prerands
@pytest.mark.parametrize('method', ['unconstrained', 'pure_con', 'pseudo_con'])
def test_request_subsets_creates_subsets(setup_expstim_cat, mocker, method):

    mock_prerands = mocker.patch('stim_randomizer.core.ExPrerands')
    experiment = setup_expstim_cat

    experiment.request_prerands(5, method)

    mock_prerands.return_value.create_prerands.assert_called_with(5, experiment.categories, method)
    mock_prerands.return_value.create_prerands.assert_called_once()

