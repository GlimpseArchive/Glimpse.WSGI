from os.path import dirname

from nose.tools import istest, assert_equal, assert_in, assert_raises

from glimpse.staticresource import StaticResource

@istest
def handling_static_resources_returns_contents_of_file():
    test_file_path = _test_file_path('test.txt')
    with open(test_file_path) as test_file:
        expected = test_file.read()
    resource = StaticResource(test_file_path)
    assert_equal(expected, resource.handle(None))

@istest
def detected_content_type_matches_file_type():
    test_file_name = 'test.png'
    expected = ('content-type', 'image/png')
    resource = StaticResource(test_file_name)
    headers = resource.get_headers()
    assert_in(expected, headers)

@istest
def handler_throws_error_when_mimetype_is_unclear():
    test_file_name = 'test'
    with assert_raises(ValueError):
        resource = StaticResource(test_file_name)

def _test_file_path(file_name):
    return dirname(__file__) + '/' + file_name
