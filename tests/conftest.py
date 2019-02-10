import pytest
import tempfile
import shutil

from stim_randomizer.core import ExpStim


categories = ['animal', 'human', 'nature']


@pytest.fixture(scope='session')
def setup_cat_dir():
    """Setup a tmpdir with named files according to the categories"""
    test_dir = tempfile.mkdtemp()

    for category in categories:
        for i in range(100):
            tempfile.mkstemp(prefix=(category + '_%02d' % i), dir=test_dir)

    yield test_dir

    shutil.rmtree(test_dir)


@pytest.fixture(scope='session')
def setup_plain_dir():
    """Setup a tmpdir with unnamed files"""
    test_dir = tempfile.mkdtemp()

    for i in range(100):
        tempfile.mkstemp(dir=test_dir)

    yield test_dir

    shutil.rmtree(test_dir)


@pytest.fixture(scope='module',
                params=[categories, None])
def setup_expstim_cat(setup_cat_dir, request):
    """Create an instance of ExpStim using mock stim with categories, once providing the categories and once
    without providing them
    """
    test_obj = ExpStim(str(setup_cat_dir), request.param)

    return test_obj


@pytest.fixture(scope='module')
def setup_expstim_plain(setup_plain_dir):
    """Create an instance of ExpStim using mock stim without categories"""
    test_obj = ExpStim(str(setup_plain_dir))

    return test_obj
