from os.path import dirname

from glimpse import log
from glimpse.staticresource import StaticResource
from glimpse.metadataresource import MetadataResource
from glimpse.requestresource import RequestResource
from glimpse.resourceconfiguration import resource_configuration
from glimpse.resourceconfiguration import ResourceDefinition

def _resource(file_name):
    path = '{0}/../static_files/{1}'.format(dirname(__file__), file_name)
    return StaticResource(path)

class Configuration(object):
    _script_sources = [
        'glimpse.js',
        'metadata?callback=glimpse.data.initMetadata',
        'request/{request_id}'
    ]

    def __init__(self):
        self.build_site()

    def build_site(self):
        resource_configuration.default_resource = _resource('404.txt')

        def add_resource_definition(*args, **kwargs):
            resource_configuration.add(ResourceDefinition(*args, **kwargs))
        
        add_resource_definition('logo', 'logo.png', _resource('logo.png'))
        add_resource_definition('sprite', 'sprite.png', _resource('sprite.png'))
        add_resource_definition('client', 'glimpse.js', _resource('glimpse.js'))
        add_resource_definition(
            name='request',
            endpoint='request',
            url_template='request/{requestId}',
            resource = RequestResource()
        )
        add_resource_definition(
            name='metadata',
            endpoint='metadata',
            url_template='metadata?{&callback}',
            resource=MetadataResource()
        )

    def generate_script_tags(self, request_id):
        log.debug('Generating script tags with request id %s', request_id)
        script_tag = '<script type="text/javascript" src="/glimpse/{0}"></script>'
        tag_list = []
        for source in self._script_sources:
            source_with_request_id = source.format(request_id=request_id)
            tag_list.append(script_tag.format(source_with_request_id))

        return ''.join(tag_list)

configuration = Configuration()
