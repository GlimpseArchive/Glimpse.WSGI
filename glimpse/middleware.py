import re

from configuration import Configuration
from staticresource import StaticResource

from os.path import dirname

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
        self._application = application
        self._config = Configuration()

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/glimpse'):
            return self._execute_resource(environ, start_response)
        # elif self.inject_client(environ):

        def filter_data(data):
            body_with_script = self._config.generate_script_tags() + '</body>'
            return data.replace('</body>', body_with_script)

        def start_glimpse_response(status, response_headers, exc_info=None):
            write = start_response(status, response_headers, exc_info)

            def glimpse_write(data):
                write(filter_data(data))

            return glimpse_write
        
        data = self._application(environ, start_glimpse_response)
        return (filter_data(item) for item in data)

    def _execute_resource(self, environ, start_response):
        resource_url = environ['PATH_INFO'][len('/glimpse'):].lstrip('/')

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
