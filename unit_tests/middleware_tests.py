from cStringIO import StringIO

from nose.tools import istest, assert_equal

import glimpse.middleware
from glimpse.middleware import Middleware
from glimpse.configuration import Configuration

@istest
def wsgi_test_environment_behaves_correctly():
    application = create_application()
    data = output_from_application(application)
    assert_equal('<html><body></body></html>', data)

@istest
def middleware_inserts_script_tags_in_returned_data():
    middleware = create_middleware()
    response = output_from_application(middleware)
    script_tags = Configuration().generate_script_tags()
    expected = '<html><body>{0}</body></html>'.format(script_tags)
    assert_equal(expected, response)

@istest
def middleware_forwards_appropriate_requests_to_resources():
    test_resources = [('^(?P<name>\w+)?', UrlBasedGreeterResource())]

    middleware = create_middleware(test_resources)

    default_response = output_from_application(middleware, '/glimpse')
    assert_equal(default_response, 'Hello, World!')

    named_response = output_from_application(middleware, '/glimpse/Nik')
    assert_equal(named_response, 'Hello, Nik!')

class UrlBasedGreeterResource(object):
    def get_headers(self):
        return [('content-type', 'text/plain')]

    def handle(self, request, name='World'):
        return 'Hello, {0}!'.format(name)

@istest
def middleware_passes_query_data_to_resources():
    test_resources = [('^$', QueryBasedGreeterResource())]

    middleware = create_middleware(test_resources)

    response = output_from_application(middleware, '/glimpse/?name=Nik')
    assert_equal(response, 'Hello, Nik!')

class QueryBasedGreeterResource(object):
    def get_headers(self):
        return [('content-type', 'text/plain')]

    def handle(self, request):
        return 'Hello, {0}!'.format(request.query_data['name'])


def create_application():
    def application(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return ['<html><body></body></html>']

    return application

def create_middleware(resources=None):
    middleware = Middleware(create_application())
    if resources is not None:
        middleware._resources = resources
    return middleware

def output_from_application(application, request_path='/'):
    output = StringIO()

    environ = {}
    request_parts = request_path.split('?')
    environ['PATH_INFO'] = request_parts[0]
    if len(request_parts) > 1:
        environ['QUERY_STRING'] = request_parts[1]

    def start_response(status, response_headers, exc_info=None):
        return output.write

    data = application(environ, start_response)
    
    for item in data:
        output.write(item)

    response = output.getvalue()
    output.close()
    return response
