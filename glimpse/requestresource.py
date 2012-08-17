import json

from glimpse.requeststore import request_store

class RequestResource(object):
    def handle(self, request, request_id=None):
        response_data = request_store.get(request_id, None)
        
        if response_data is None:
            request.response_status = '404 Not Found'
            content_type = 'text/plain'
            response_data = 'No Resource Exists with that ID'
        else:
            content_type = 'application/json'
            response_with_id = response_data.copy()
            response_with_id['requestId'] = request_id
            response_data = json.dumps(response_with_id)

        request.response_headers['content-type'] = content_type
        return response_data
            
