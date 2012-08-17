import json

from glimpse.requeststore import request_store

class RequestResource(object):
    def handle(self, request, request_id=None):
        response_data = request_store.get(request_id, None)
        if response_data is None:
            request.response_status = '404 Not Found'
            request.response_headers['content-type'] = 'text/plain'
            return 'No Resource Exists with that ID'
        else:
            request.response_headers['content-type'] = 'application/json'
            response_with_id = response_data.copy()
            response_with_id['requestId'] = request_id
            return json.dumps(response_with_id)
            
