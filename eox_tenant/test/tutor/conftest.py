import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    """
    Makes the tests reuse the existing database
    """
    pass
