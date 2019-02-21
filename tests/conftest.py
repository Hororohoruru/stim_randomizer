import pytest
import tempfile
import shutil

from stim_randomizer.core import ExpStim, ExpSets, ExPrerands


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


@pytest.fixture(scope='module',
                params=['parent', 'child'])
def setup_expsets_cat(setup_cat_dir, request):
    """Create an instance of ExpSets using mock stim with categories"""
    test_obj = ExpSets(str(setup_cat_dir), request.param)

    yield test_obj

    shutil.rmtree(test_obj.out_dir)


@pytest.fixture(scope='module',
                params=['parent', 'child'])
def setup_exprerands_from_subsets(setup_expsets_cat, request):
    """Create an instance of ExPrerands from ExpSets susing mock stim with categories"""
    test_obj = ExPrerands(setup_expsets_cat.root_path, setup_expsets_cat.out_dir, request.param)

    yield test_obj

    shutil.rmtree(test_obj.out_dir)


@pytest.fixture(scope='module')
def setup_exprerands_from_expstim(setup_expstim_cat):
    """Create an instance of ExPrerands without subsets from ExpStim susing mock stim with categories"""
    test_obj = ExPrerands(setup_expstim_cat.path, setup_expstim_cat.subsets, 'parent')

    yield test_obj

    shutil.rmtree(test_obj.out_dir)
