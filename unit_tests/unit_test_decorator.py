from functools import wraps

from nose.tools import istest

from glimpse.configuration import Configuration
from glimpse import middleware

def test_with_resources(resources):
    def wrap(function):
        function = istest(function)
        @wraps(function)
        def wrapper(*args, **kwargs):
            initial_resources = middleware.configuration.resources
            middleware.configuration.resources = resources
            try:
                function(*args, **kwargs)
            finally:
                middleware.configuration.resources = initial_resources
        return wrapper
    return wrap
