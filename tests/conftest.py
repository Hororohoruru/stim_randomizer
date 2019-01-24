import pytest
import tempfile

from stim_randomizer.ExpStim import ExpStim


categories = ['animal', 'human', 'nature']


@pytest.fixture()
def setup_cat_dir():
    test_dir = tempfile.mkdtemp()

    for category in categories:
        for i in range(10):
            tempfile.mkstemp(prefix=(category + '_%02d' % i), dir=test_dir)

    return test_dir


@pytest.fixture()
def setup_plain_dir():
    test_dir = tempfile.mkdtemp()

    for i in range(10):
        tempfile.mkstemp(dir=test_dir)

    return test_dir


@pytest.fixture()
def setup_cat(setup_cat_dir):

    test_obj = ExpStim(str(setup_cat_dir), categories)

    return test_obj


@pytest.fixture()
def setup_plain(setup_plain_dir):

    test_obj = ExpStim(str(setup_plain_dir))

    return test_obj
