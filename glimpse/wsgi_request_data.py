from glimpse.requeststore import request_store

def _request_tab_data(environ):
    return {
        'Glimpse.WSGI.Tab.Request': {
            'data': _data_from_environ(environ),
            'name': 'Request'
        }
    }

def _data_from_environ(environ):
    environ_variables = ['REQUEST_METHOD', 'SCRIPT_NAME', 'PATH_INFO',
                         'QUERY_STRING', 'CONTENT_TYPE', 'CONTENT_TYPE',
                         'CONTENT_TYPE', 'CONTENT_LENGTH', 'SERVER_NAME',
                         'SERVER_PORT', 'SERVER_PROTOCOL']
    environ_data = {variable: environ[variable]
                    for variable in environ_variables
                    if environ.get(variable, None) is not None}

    return environ_data

def inject_data_from_environ(request_id, environ):
    request_in_store = request_store.get(request_id, None)
    if request_in_store is None:
        raise Exception()

    request_data = request_in_store.get('data', None)
    if request_data is None:
        request_in_store['data'] = {}
        request_data = request_in_store['data']

    request_data.update(_request_tab_data(environ))
