from os.path import dirname

from nose.tools import istest, assert_equal, assert_in, assert_raises

from glimpse.middleware import _Request
from glimpse.staticresource import StaticResource

@istest
def content_type_matches_mimetype():
    request = _Request(None)
    resource = StaticResource(_test_file_path('test.txt'))
    resource.handle(request)
    response_headers = request.get_response_header_list()
    assert_in(('content-type', 'text/plain'), response_headers)

@istest
def handling_static_resources_returns_contents_of_file():
    test_file_path = _test_file_path('test.txt')
    with open(test_file_path) as test_file:
        expected = test_file.read()
    resource = StaticResource(test_file_path)
    assert_equal(expected, resource.handle(_Request(None)))

@istest
def handler_throws_error_when_mimetype_is_unclear():
    test_file_name = 'test'
    with assert_raises(ValueError):
        resource = StaticResource(test_file_name)

def _test_file_path(file_name):
    return dirname(__file__) + '/' + file_name
