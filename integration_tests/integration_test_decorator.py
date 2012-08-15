from threading import Thread
from time import sleep
from wsgiref.simple_server import make_server
from functools import wraps
from os.path import dirname

from nose.tools import istest

import sys
sys.path.insert(0, dirname(__file__) + '/djangotestapplication')

from testsite.wsgi import application

PORT = 8001

class ApplicationServerThread(Thread):
    def __init__(self, *args, **kwargs):
        super(ApplicationServerThread, self).__init__(*args, **kwargs)
        self._server = make_server(host='', port=PORT, app=application)

    def run(self):
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        sleep(0.000001) #TODO: Otherwise run_tests.sh says address in use.
        # I don't know why this is. It should probably be fixed.

def test(function):
    function = istest(function)
    @wraps(function)
    def wrapper(*args, **kwargs):
        server_thread = ApplicationServerThread()
        server_thread.start()
        try:
            function(*args, **kwargs)
        finally:
            server_thread.stop()
            server_thread.join()
    return wrapper
