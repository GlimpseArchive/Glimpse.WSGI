from uuid import uuid4
import json

from nose.tools import istest, assert_equal, assert_in

from glimpse.middleware import _Request
from glimpse.requestresource import RequestResource
from glimpse.requeststore import request_store

@istest
def returns_correct_data_from_request_store():
    uuid = uuid4().hex
    request_store[uuid] = {
        'statusCode': 200,
        'data': {
            'glimpse.tab' : 'test_tab'
        }
    }

    request_resource = RequestResource()

    response = request_resource.handle(_Request(''), uuid)
    expected_response = request_store[uuid]
    expected_response['requestId'] = uuid

    assert_equal(response, json.dumps(expected_response))
