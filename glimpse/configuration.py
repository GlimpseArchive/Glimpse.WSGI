from os.path import dirname

from glimpse.staticresource import StaticResource
from glimpse.metadataresource import MetadataResource

def _resource(file_name):
    path = '{0}/../static_files/{1}'.format(dirname(__file__), file_name)
    return StaticResource(path)

class ResourceDefinition(object):
    def __init__(self, name, endpoint, resource, url_template=None):
        self.name = name
        self.endpoint = endpoint
        self.resource = resource
        self.url_template = url_template or endpoint

class Configuration(object):
    ''' resources is a list of triples of the resource name, the endpoint and
    then the resource object for handling the request.'''

    resources = [
        ResourceDefinition('logo', 'logo.png', _resource('logo.png')),
        ResourceDefinition('sprite', 'sprite.png', _resource('sprite.png')),
        ResourceDefinition('client', 'glimpse.js', _resource('glimpse.js')),
        ResourceDefinition(
            name='metadata',
            endpoint='metadata',
            url_template='metadata{&callback}',
            resource=MetadataResource()
        )
    ]
    default_resource = _resource('404.txt')

    _script_sources = [
        'glimpse.js',
        'metadata?callback=glimpse.data.initMetadata'
    ]

    @staticmethod
    def _generate_resource_metadata(resource_definitions):
        return {'glimpse_' + definition.name:
                '/glimpse/' + definition.url_template
                for definition in resource_definitions}           

    def get_metadata(self):
        pass

    def generate_script_tags(self):
        script_tag = '<script type="text/javascript" src="/glimpse/{0}"></script>'
        tag_list = (script_tag.format(source) 
                    for source in self._script_sources)
        return ''.join(tag_list)

configuration = Configuration()
