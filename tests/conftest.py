#
from rest_framework.test import APIClient

import pytest


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass

@pytest.fixture
def http_client():
    return APIClient()
