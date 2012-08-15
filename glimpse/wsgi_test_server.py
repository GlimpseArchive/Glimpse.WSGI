from cStringIO import StringIO

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
