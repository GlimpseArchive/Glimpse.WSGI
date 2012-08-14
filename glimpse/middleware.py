from configuration import Configuration

class Middleware(object):
    def __init__(self, application):
        self._application = application
        self._config = Configuration()

    def __call__(self, environ, start_response):
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

def wrap_application(wsgi_application):
    return Middleware(wsgi_application)
