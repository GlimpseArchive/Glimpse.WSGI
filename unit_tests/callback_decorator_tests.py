from nose.tools import istest, assert_equal

from glimpse.callback_decorator import callbackenabled

@istest
def callback_in_query_string_is_used():
    query_string = {'callback' : 'callback_function'}
    request = TestRequest(query_string)
    resource = GreeterResource()
    response = resource.handle(request)
    assert_equal('callback_function("Hello world")', response)

class GreeterResource(object):
    @callbackenabled
    def handle(self, request):
        return '"Hello world"'

class TestRequest(object):
    def __init__(self, query_data):
        self.query_data = query_data
