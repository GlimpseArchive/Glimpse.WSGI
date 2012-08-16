from functools import wraps

from nose.tools import istest

from glimpse import resourceconfiguration

def test_with_resources(resources):
    def wrap(function):
        function = istest(function)
        @wraps(function)
        def wrapper(*args, **kwargs):
            initial_resources = resourceconfiguration.resource_configuration.resource_definitions
            resourceconfiguration.resource_configuration.resource_definitions = resources
            try:
                function(*args, **kwargs)
            finally:
                resourceconfiguration.resource_configuration.resource_definitions = initial_resources
        return wrapper
    return wrap
