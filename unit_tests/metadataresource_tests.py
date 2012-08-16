from nose.tools import istest, assert_equal, assert_in

from glimpse.metadataresource import MetadataResource
from glimpse.resourceconfiguration import resource_configuration
from unit_test_decorator import test_with_resources
from resource_configuration_tests import resources, resources_as_dict

@test_with_resources(resources)
def can_get_metadata_as_dict():
    expected_resources = resource_configuration._add_unimplemented_resources(
        resources_as_dict
    )
    expected = {
        'plugins' : { },
        'resources' : expected_resources
    }
    
    assert_equal(expected, MetadataResource()._get_metadata())
