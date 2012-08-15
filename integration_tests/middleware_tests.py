from os.path import dirname

import requests
from nose.tools import assert_equal, assert_in

from integration_test_decorator import test, PORT

@test
def static_files_are_served_correctly():
    file_names = ['logo.png', 'sprite.png', 'glimpse.js']

    for file_name in file_names:
        request = requests.get(_resource_url(file_name))
        assert_equal(200, request.status_code)

        file_path = dirname(__file__) + '/../static_files/' + file_name
        with open(file_path, 'rb') as static_file:
            assert_equal(static_file.read(), request.content)

@test
def script_files_are_inserted():
    request = requests.get(_application_url())
    script_tag = '<script type="text/javascript" src="/glimpse/glimpse.js">'
    script_tag += '</script>'
    script_tag += '<script type="text/javascript" '
    script_tag += 'src="/glimpse/metadata?callback=glimpse.data.initMetadata">'
    script_tag += '</script>'
    assert_in(script_tag, request.text)

@test
def metadata_endpoint_exists():
    request = requests.get(_resource_url('metadata'))
    assert_equal(200, request.status_code)

def _resource_url(resource):
    return _application_url('glimpse/' + resource)

def _application_url(query=''):
    return 'http://localhost:{0}/{1}'.format(PORT, query)
