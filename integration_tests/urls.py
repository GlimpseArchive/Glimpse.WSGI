from integration_test_decorator import PORT

def resource_url(resource):
    return application_url('glimpse/' + resource)

def application_url(query=''):
    return 'http://localhost:{0}/{1}'.format(PORT, query)
