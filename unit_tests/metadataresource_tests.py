from nose.tools import istest, assert_equal, assert_in

from glimpse.metadataresource import MetadataResource
from glimpse.resourceconfiguration import resource_configuration
from glimpse.middleware import _Request
from unit_test_decorator import test_with_resources
from resource_configuration_tests import resources, resources_as_dict

@test_with_resources(resources)
def can_get_metadata_as_dict():
    expected_resources = resource_configuration._add_unimplemented_resources(
        resources_as_dict
    )
    expected = {
        'version': '0.0.1',
        'plugins': { },
        'resources': expected_resources
    }
    
    assert_equal(expected, MetadataResource()._get_metadata())

@istest
def content_type_is_correct():
    query_datas = [{'callback': 'initMetadata'}, {}]
    content_types = ['application/x-javascript', 'application/json']
    for query_data, content_type in zip(query_datas, content_types):
        request = _Request(query_data)
        metadata_resource = MetadataResource()
        metadata_resource.handle(request)
        response_headers = request.get_response_header_list()
        assert_in(('content-type', content_type), response_headers)
