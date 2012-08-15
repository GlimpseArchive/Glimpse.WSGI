def create_application():
    def application(environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return ['<html><body></body></html>']

    return application
