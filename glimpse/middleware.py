import re

from configuration import Configuration
from staticresource import StaticResource

from os.path import dirname
from glimpse import log

def _resource(file_name):
    path = '{0}/../static_files/{1}'.format(dirname(__file__), file_name)
    return StaticResource(path)

class Middleware(object):
    _resources = [
        ('^logo\.png', _resource('logo.png')),
        ('^sprite\.png', _resource('sprite.png')),
        ('^glimpse\.js', _resource('glimpse.js'))
    ]
    _default_resource = _resource('404.txt')

    def __init__(self, application):
        log.info('Loading Glimpse middleware')
        self._application = application
        self._config = Configuration()

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/glimpse'):
            return self._execute_resource(environ, start_response)
        else:
            return self._hook_into_application(environ, start_response)

    def _hook_into_application(self, environ, start_response):
        log.info('Passing request to application')
        def start_glimpse_response(status, response_headers, exc_info=None):
            lowered_headers = [(key.lower(), value.lower()) 
                               for key, value in response_headers]
            write = start_response(status, response_headers, exc_info)

            if ('content-type', 'text/html') in lowered_headers:
                middleware_write = lambda data: write(self._filter_data(data))
            else:
                middleware_write = write

            return middleware_write
        
        data = self._application(environ, start_glimpse_response)
        return (self._filter_data(item) for item in data)

    def _filter_data(self, data):
        body_with_script = self._config.generate_script_tags() + '</body>'
        return data.replace('</body>', body_with_script)

    def _execute_resource(self, environ, start_response):
        resource_url = environ['PATH_INFO'][len('/glimpse'):].lstrip('/')
        log.info('Got a request for {0}'.format(resource_url))

        for url_pattern, resource in self._resources:
            matching = re.match(url_pattern, resource_url)
            if matching is not None:
                start_response('200 OK', resource.get_headers())
                matched_arguments = {key: value for key, value 
                                     in matching.groupdict().iteritems()
                                     if value is not None}
                return [resource.handle(**matched_arguments)]

        start_response('404 No matching resource',
                       self._default_resource.get_headers())
        return [self._default_resource.handle()]

def wrap_application(wsgi_application):
    return Middleware(wsgi_application)
