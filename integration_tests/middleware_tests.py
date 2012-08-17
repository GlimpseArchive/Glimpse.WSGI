from os.path import dirname

import requests
from nose.tools import assert_equal, assert_in

from integration_test_decorator import test
from urls import resource_url, application_url

@test
def static_files_are_served_correctly():
    file_names = ['logo.png', 'sprite.png', 'glimpse.js']

    for file_name in file_names:
        request = requests.get(resource_url(file_name))
        assert_equal(200, request.status_code)

        file_path = dirname(__file__) + '/../static_files/' + file_name
        with open(file_path, 'rb') as static_file:
            assert_equal(static_file.read(), request.content)

@test
def script_tags_are_inserted():
    request = requests.get(application_url())
    request_id = request.headers['x-glimpse-requestid']
    script_sources = ['glimpse.js',
                      'metadata?callback=glimpse.data.initMetadata',
                      'request/{0}'.format(request_id)]
    script_tags = ''.join([_script_tag(source) for source in script_sources])
    assert_in(script_tags, request.text)

def _script_tag(source):
    tag_template = '<script type="text/javascript" src="/glimpse/{0}"></script>'
    return tag_template.format(source)
