from nose.tools import istest, assert_equal

from glimpse.middleware import _Request
from glimpse.callback_decorator import callbackenabled

@istest
def callback_in_query_string_is_used():
    query_data = {'callback' : 'callback_function'}
    request = _Request(query_data)
    resource = GreeterResource()
    response = resource.handle(request)
    assert_equal('callback_function("Hello world");', response)

class GreeterResource(object):
    @callbackenabled
    def handle(self, request):
        request.response_headers['content-type'] = 'text/plain'
        return '"Hello world"'
