from nose.tools import istest, assert_equal, assert_in

from glimpse.configuration import configuration, ResourceDefinition
from unit_test_decorator import test_with_resources

_resources = [
    ResourceDefinition('logo', 'logo.png', None),
    ResourceDefinition(
        name='metadata',
        endpoint='metadata',
        url_template='metadata{&callback}',
        resource=None
    )
]

_resources_as_dict = {
    'glimpse_logo': '/glimpse/logo.png',
    'glimpse_metadata': '/glimpse/metadata{&callback}'
}

@istest
def can_generate_resource_metadata_from_definitions():
    generate_metadata = configuration._generate_resource_metadata

    assert_equal(_resources_as_dict, generate_metadata(_resources))

@istest
def can_add_unimplemented_resources():
    all_resource_metadata = configuration._add_unimplemented_resources(
        _resources_as_dict
    )
    expected_entry = (
        'glimpse_history', 'NEED TO IMPLEMENT RESOURCE glimpse_history'
    )

    assert_in(expected_entry, all_resource_metadata.items())

@test_with_resources(_resources)
def can_get_metadata_as_dict():
    expected_resources = configuration._add_unimplemented_resources(
        _resources_as_dict
    )
    expected = {
        'plugins' : { },
        'resources' : expected_resources
    }
    
    assert_equal(expected, configuration.get_metadata())
