from mimetypes import guess_type

class StaticResource(object):
    def __init__(self, file_name, mimetype=None):
        self._file_name = file_name
        self._mimetype = mimetype or guess_type(file_name)[0]
        if self._mimetype is None:
            raise ValueError('No mimetype provided and cannot guess mimetype')

    def handle(self, request):
        request.response_headers['content-type'] = self._mimetype
        with open(self._file_name) as resource_file:
            return resource_file.read()
