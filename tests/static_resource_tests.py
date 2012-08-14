from nose.tools import istest, assert_equal

from glimpse.staticresource import StaticResource

@istest
def handling_static_resources_returns_contents_of_file():
    test_file_name = 'test.txt'
    with open(test_file_name) as test_file:
        expected = test_file.read()
    resource = StaticResource(test_file_name)
    assert_equal(expected, resource.handle())

@istest
def detected_content_type_matches_file_type():
    test_file_name = 'test.png'
    expected = 'image/png'
    resource = StaticResource(test_file_name)
    content_type = resource.get_headers()['content-type']
    assert_equal(expected, content_type)
