import requests

from nose.tools import assert_in, assert_equal

from integration_test_decorator import test
from urls import application_url, resource_url

@test
def request_resource_returns_json_about_given_request():
    request = requests.get(application_url())
    assert_in('x-glimpse-requestid', request.headers)
    request_id = request.headers['x-glimpse-requestid']

    request = requests.get(resource_url('request/{}'.format(request_id)))
    assert_equal(200, request.status_code)
    assert_equal('application/json', request.headers['content-type'])
