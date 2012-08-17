import json

from glimpse.callback_decorator import callbackenabled
from glimpse.resourceconfiguration import resource_configuration

class MetadataResource(object):
    @callbackenabled
    def handle(self, request):
        request.response_headers['content-type'] = 'application/json'
        return json.dumps(self._get_metadata())

    def _get_metadata(self):
        resource_metadata = resource_configuration.get_resource_metadata()
        metadata = {
            'version': '0.0.1',
            'plugins': {},
            'resources': resource_metadata
        }
        return metadata
