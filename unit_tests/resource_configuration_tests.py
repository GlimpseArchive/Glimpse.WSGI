from nose.tools import istest, assert_equal, assert_in

from glimpse.resourceconfiguration import ResourceDefinition
from glimpse.resourceconfiguration import ResourceConfiguration

resources = [
    ResourceDefinition('logo', 'logo.png', None),
    ResourceDefinition(
        name='metadata',
        endpoint='metadata',
        url_template='metadata{&callback}',
        resource=None
    )
]

resources_as_dict = {
    'glimpse_logo': '/glimpse/logo.png',
    'glimpse_metadata': '/glimpse/metadata{&callback}'
}

@istest
def can_generate_resource_metadata_from_definitions():
    test_configuration = get_test_configuration()
    expected = test_configuration._add_unimplemented_resources(resources_as_dict)

    assert_equal(expected, test_configuration.get_resource_metadata())

@istest
def can_add_unimplemented_resources():
    test_configuration = get_test_configuration()
    all_resource_metadata = test_configuration._add_unimplemented_resources(
        resources_as_dict
    )
    expected_entry = (
        'glimpse_history', 'NEED TO IMPLEMENT RESOURCE glimpse_history'
    )

    assert_in(expected_entry, all_resource_metadata.items())


def get_test_configuration():
    test_configuration = ResourceConfiguration()
    for resource_definition in resources:
        test_configuration.add(resource_definition)
    return test_configuration
