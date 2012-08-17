from nose.tools import istest, assert_equal

from glimpse.configuration import configuration
from glimpse.resourceconfiguration import resource_configuration
from glimpse.resourceconfiguration import ResourceDefinition
from glimpse.middleware import Middleware
from unit_test_decorator import test_with_resources
from application_creation import create_application
from wsgi_test_server import output_from_application

@istest
def wsgi_test_environment_behaves_correctly():
    application = create_application()
    data = output_from_application(application)
    assert_equal('<html><body></body></html>', data)

@istest
def middleware_inserts_script_tags_in_returned_data():
    middleware = Middleware(create_application())
    response = output_from_application(middleware)
    script_tags = configuration.generate_script_tags('uuid')
    expected = '<html><body>{0}</body></html>'.format(script_tags)
    assert_equal(expected, response)

class UrlBasedGreeterResource(object):
    def handle(self, request, name='World'):
        request.response_headers['content-type'] = 'text/plain'
        return 'Hello, {0}!'.format(name)

@test_with_resources([ResourceDefinition('', '', UrlBasedGreeterResource())])
def middleware_forwards_appropriate_requests_to_resources():
    middleware = Middleware(create_application())

    default_response = output_from_application(middleware, '/glimpse')
    assert_equal(default_response, 'Hello, World!')

    named_response = output_from_application(middleware, '/glimpse/Nik')
    assert_equal(named_response, 'Hello, Nik!')

class QueryBasedGreeterResource(object):
    def handle(self, request):
        request.response_headers['content-type'] = 'text/plain'
        return 'Hello, {0}!'.format(request.query_data['name'])

@test_with_resources([ResourceDefinition('', '', QueryBasedGreeterResource())])
def middleware_passes_query_data_to_resources():
    middleware = Middleware(create_application())

    response = output_from_application(middleware, '/glimpse/?name=Nik')
    assert_equal(response, 'Hello, Nik!')

@istest
def arguments_are_properly_extracted():
    match_url = Middleware(None)._match_url

    assert_equal(None, match_url('client', '/id/12'))
    assert_equal(None, match_url('cli', '/client/12'))
    assert_equal(None, match_url('cli', '/client'))
    assert_equal(['12', 'add'], match_url('id', '/id/12/add/'))
    assert_equal(['12', 'add'], match_url('id', '/id/12/add'))
    assert_equal(['12', 'add'], match_url('', '/12/add/'))
    assert_equal([], match_url('', ''))
    assert_equal([], match_url('', '/'))
