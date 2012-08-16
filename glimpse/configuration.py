from os.path import dirname

from glimpse.staticresource import StaticResource
from glimpse.metadataresource import MetadataResource
from glimpse.resourceconfiguration import resource_configuration
from glimpse.resourceconfiguration import ResourceDefinition

def _resource(file_name):
    path = '{0}/../static_files/{1}'.format(dirname(__file__), file_name)
    return StaticResource(path)

class Configuration(object):
    _script_sources = [
        'glimpse.js',
        'metadata?callback=glimpse.data.initMetadata'
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
            name='metadata',
            endpoint='metadata',
            url_template='metadata{&callback}',
            resource=MetadataResource()
        )

    def generate_script_tags(self):
        script_tag = '<script type="text/javascript" src="/glimpse/{0}"></script>'
        tag_list = (script_tag.format(source) 
                    for source in self._script_sources)
        return ''.join(tag_list)

configuration = Configuration()
