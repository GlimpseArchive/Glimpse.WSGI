from os.path import dirname

from glimpse.callback_decorator import callbackenabled

class DummyResource(object):
    @callbackenabled
    def handle(self, request):
        request.response_headers['content-type'] = 'application/x-javascript'
        dummy_file_name = '{0}/dummydata.txt'.format(dirname(__file__))
        with open(dummy_file_name) as dummy_file:
            return dummy_file.read()
