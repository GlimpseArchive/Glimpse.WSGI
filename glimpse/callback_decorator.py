from functools import wraps

def callbackenabled(handle_function):
    @wraps(handle_function)
    def wrapper(self, request, *args, **kwargs):
        result = handle_function(self, request, *args, **kwargs)
        callback = request.query_data.get('callback', None)
        if callback is None:
            return result
        else:
            return '{0}({1});'.format(callback, result)
    return wrapper
