from os.path import dirname

from glimpse.staticresource import StaticResource

def _resource(file_name):
    path = '{0}/../static_files/{1}'.format(dirname(__file__), file_name)
    return StaticResource(path)

class Configuration(object):
    resources = [
        ('^logo\.png', _resource('logo.png')),
        ('^sprite\.png', _resource('sprite.png')),
        ('^glimpse\.js', _resource('glimpse.js'))
    ]
    default_resource = _resource('404.txt')

    def generate_script_tags(self):
        return '<script type="text/javascript" src="/glimpse/glimpse.js"></script>'

configuration = Configuration()
