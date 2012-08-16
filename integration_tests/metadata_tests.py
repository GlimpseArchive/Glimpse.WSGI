import json

import requests
from nose.tools import assert_equal

from integration_test_decorator import test
from urls import resource_url
from glimpse.resourceconfiguration import resource_configuration

@test
def metadata_endpoint_exists():
    request = requests.get(resource_url('metadata'))
    assert_equal(200, request.status_code)

@test
def correct_metadata_is_returned():
    metadata = {
        'plugins': {},
        'resources': resource_configuration.get_resource_metadata()
    }
    expected = 'glimpse.data.initMetadata({0});'.format(json.dumps(metadata))

    url = resource_url('metadata?callback=glimpse.data.initMetadata')
    request = requests.get(url)

    assert_equal(expected, request.text)
