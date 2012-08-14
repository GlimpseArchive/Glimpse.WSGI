from nose.tools import istest, assert_equal

from glimpse.staticresource import StaticResource

@istest
def handling_static_resources_returns_contents_of_file():
    test_file_name = 'test.txt'
    with open(test_file_name) as test_file:
        expected = test_file.read()
    resource = StaticResource(test_file_name)
    assert_equal(expected, resource.handle())

    
