from os.path import dirname

import requests
from nose.tools import assert_equal, assert_in

from test_decorator import test, PORT

@test
def static_files_are_served_correctly():
    file_names = ['logo.png', 'sprite.png', 'glimpse.js']

    for file_name in file_names:
        url = 'http://localhost:{0}/glimpse/{1}'.format(PORT, file_name)
        request = requests.get(url)
        assert_equal(200, request.status_code)

        file_path = dirname(__file__) + '/../static_files/' + file_name
        with open(file_path, 'rb') as static_file:
            assert_equal(static_file.read(), request.content)

@test
def script_files_are_inserted():
    request = requests.get('http://localhost:{0}/'.format(PORT))
    script_tag = '<script type="text/javascript" src="/glimpse/glimpse.js">'
    script_tag += '</script>'
    assert_in(script_tag, request.text)
