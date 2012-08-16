import json

from glimpse.callback_decorator import callbackenabled
from glimpse.resourceconfiguration import resource_configuration

class MetadataResource(object):
    @callbackenabled
    def handle(self, request):
        return json.dumps(self._get_metadata())

    def get_headers(self):
        return [('content-type', 'application/x-javascript')]

    def _get_metadata(self):
        resource_metadata = resource_configuration.get_resource_metadata()
        metadata = {
            'plugins': {},
            'resources': resource_metadata
        }
        return metadata
