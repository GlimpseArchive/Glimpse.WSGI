from os.path import dirname

from glimpse.staticresource import StaticResource
from glimpse.metadataresource import MetadataResource

def _resource(file_name):
    path = '{0}/../static_files/{1}'.format(dirname(__file__), file_name)
    return StaticResource(path)

class Configuration(object):
    resources = [
        ('^logo\.png', _resource('logo.png')),
        ('^sprite\.png', _resource('sprite.png')),
        ('^glimpse\.js', _resource('glimpse.js')),
        ('^metadata', MetadataResource())
    ]
    default_resource = _resource('404.txt')

    _script_sources = [
        'glimpse.js',
        'metadata?callback=glimpse.data.initMetadata'
    ]

    def generate_script_tags(self):
        script_tag = '<script type="text/javascript" src="/glimpse/{0}"></script>'
        tag_list = (script_tag.format(source) 
                    for source in self._script_sources)
        return ''.join(tag_list)

configuration = Configuration()
