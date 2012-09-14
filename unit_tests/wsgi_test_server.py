from cStringIO import StringIO

def _find_in_headers(header_name, headers):
    for name, value in headers:
        if header_name == name:
            return value

def output_from_application(application, request_path='/'):
    return output_and_id_from_application(application, request_path=request_path)[0]

def output_and_id_from_application(application, request_path='/'):
    output = StringIO()
    request_id = [None]
    environ = {}
    request_parts = request_path.split('?')
    environ['PATH_INFO'] = request_parts[0]
    if len(request_parts) > 1:
        environ['QUERY_STRING'] = request_parts[1]

    def start_response(status, response_headers, exc_info=None):
        request_id_header = 'x-glimpse-requestid'
        request_id[0] = _find_in_headers(request_id_header, response_headers)
        return output.write

    data = application(environ, start_response)
    
    for item in data:
        output.write(item)

    response = output.getvalue()
    output.close()
    return response, request_id[0]
