import requests
from nose.tools import assert_equal

from integration_test_decorator import test
from urls import resource_url

@test
def metadata_endpoint_exists():
    request = requests.get(resource_url('metadata'))
    assert_equal(200, request.status_code)
