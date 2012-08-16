class ResourceDefinition(object):
    def __init__(self, name, endpoint, resource, url_template=None):
        self.name = name
        self.endpoint = endpoint
        self.resource = resource
        self.url_template = url_template or endpoint

class ResourceConfiguration(object):
    _expected_resource_names = [
        'paging', 'tab', 'glimpse_client', 'glimpse_config', 'glimpse_ajax',
        'glimpse_history', 'glimpse_logo', 'glimpse_popup', 'glimpse_request',
        'glimpse_metadata', 'glimpse_sprite'
    ]

    def __init__(self):
        self.default_resource = None
        self.resource_definitions = []

    def get_resource_metadata(self):
        implemented_resources = {'glimpse_' + definition.name:
                                 '/glimpse/' + definition.url_template
                                 for definition in self.resource_definitions}
        return self._add_unimplemented_resources(implemented_resources)

    def add(self, resource_definition):
        self.resource_definitions.append(resource_definition)

    def _add_unimplemented_resources(self, resource_metadata):
        complete_metadata = {name: 'NEED TO IMPLEMENT RESOURCE ' + name
                             for name in self._expected_resource_names}
        complete_metadata.update(resource_metadata)
        return complete_metadata

resource_configuration = ResourceConfiguration()
