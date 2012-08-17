import requests
import json

from nose.tools import assert_in, assert_equal

from integration_test_decorator import test
from urls import application_url, resource_url

@test
def request_resource_returns_json_about_given_request():
    response = _send_request_to_requestresource()

    assert_equal(200, response.status_code)
    assert_equal('application/json', response.headers['content-type'])

@test
def request_resource_json_contains_information_from_environ():
    response_json = _send_request_to_requestresource().text
    response = json.loads(response_json)
    assert_in('data', response)
    assert_in('REQUEST_METHOD', response['data'])

def _send_request_to_requestresource():
    request = requests.get(application_url())
    assert_in('x-glimpse-requestid', request.headers)
    request_id = request.headers['x-glimpse-requestid']

    return requests.get(resource_url('request/{}'.format(request_id)))
