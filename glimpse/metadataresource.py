class MetadataResource(object):
    def __init__(self):
        pass

    def handle(self, request):
        return ''

    def get_headers(self):
        return [('content-type', 'application/x-javascript')]
