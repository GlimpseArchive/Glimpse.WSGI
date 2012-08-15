import re
from urlparse import parse_qs

from configuration import configuration

from glimpse import log

class Middleware(object):
    def __init__(self, application):
        log.info('Loading Glimpse middleware')
        self._application = application

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/glimpse'):
            return self._execute_resource(environ, start_response)
        else:
            return self._hook_into_application(environ, start_response)

    def _filter_data(self, data):
        body_with_script = configuration.generate_script_tags() + '</body>'
        return data.replace('</body>', body_with_script)

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

    def _execute_resource(self, environ, start_response):
        resource_url = environ['PATH_INFO'][len('/glimpse'):].lstrip('/')
        log.info('Got a request for {0}'.format(resource_url))

        query_data = self._parse_query_string(environ.get('QUERY_STRING', ''))
        request = _Request(query_data)

        resource, arguments = self._match_resource(resource_url)
        if resource is None:
            resource = configuration.default_resource
            arguments = {}
            status = '404 No matching resource'
        else:
            status = '200 OK'

        start_response(status, resource.get_headers())
        return [resource.handle(request, **arguments)]

    def _match_resource(self, resource_url):
        for url_pattern, resource in configuration.resources:
            matching = re.match(url_pattern, resource_url)
            if matching is not None:
                arguments = self._extract_arguments(matching)
                return (resource, arguments)
        return (None, None)
        
    def _extract_arguments(self, matching):
        return {key: value 
                for key, value in matching.groupdict().iteritems()
                if value is not None}

    def _parse_query_string(self, query_string):
        query_data = parse_qs(query_string)
        query_data = {key: value.pop() if len(value) == 1 else value
                      for key, value in query_data.iteritems()}
        return query_data

class _Request(object):
    def __init__(self, query_data):
        self.query_data = query_data

def wrap_application(wsgi_application):
    return Middleware(wsgi_application)
