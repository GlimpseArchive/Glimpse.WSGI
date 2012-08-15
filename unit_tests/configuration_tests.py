from nose.tools import istest, assert_equal

from glimpse.configuration import Configuration, ResourceDefinition

@istest
def can_generate_resource_metadata_from_definitions():
    generate_metadata = Configuration._generate_resource_metadata

    resources = [
        ResourceDefinition('logo', 'logo.png', None),
        ResourceDefinition(
            name='metadata',
            endpoint='metadata',
            url_template='metadata{&callback}',
            resource=None
        )
    ]

    expected = {
        "glimpse_logo": "/glimpse/logo.png",
        "metadata": "/glimpse/metadata{&callback}"
    }

    assert_equal(expected, generate_metadata(resources))
