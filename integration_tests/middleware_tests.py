from threading import Thread
from wsgiref.simple_server import make_server
from functools import wraps
from os.path import dirname

from nose.tools import istest

import sys
sys.path.insert(0, dirname(__file__) + '/djangotestapplication')

from testsite.wsgi import application

PORT = 8000

class ApplicationServerThread(Thread):
    def __init__(self, *args, **kwargs):
        super(ApplicationServerThread, self).__init__(*args, **kwargs)
        self._server = make_server(host='', port=PORT, app=application)

    def run(self):
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()

def test(function):
    function = istest(function)
    @wraps(function)
    def wrapper(*args, **kwargs):
        server_thread = ApplicationServerThread()
        server_thread.start()
        function(*args, **kwargs)
        server_thread.stop()
        server_thread.join()
    return wrapper

@test
def fake_test():
    pass
    

# @istest
# def something(): ...
# ===
# def something(): ...
# something = istest(something)

