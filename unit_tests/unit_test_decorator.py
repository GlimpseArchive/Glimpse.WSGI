from functools import wraps

from nose.tools import istest

from glimpse.configuration import Configuration
from glimpse import middleware

def test_with_resources(resources):
    def wrap(function):
        function = istest(function)
        @wraps(function)
        def wrapper(*args, **kwargs):
            initial_configuration = middleware.configuration

            test_configuration = Configuration()
            test_configuration.resources = resources
            middleware.configuration = test_configuration
            try:
                function(*args, **kwargs)
            finally:
                middleware.configuration = initial_configuration
        return wrapper
    return wrap
