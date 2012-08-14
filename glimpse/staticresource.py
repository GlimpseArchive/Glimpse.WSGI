class StaticResource(object):
    def __init__(self, file_name):
        self._file_name = file_name

    def handle(self):
        with open(self._file_name) as resource_file:
            return resource_file.read()

    def get_headers(self):

        pass
