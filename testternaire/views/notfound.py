from pyramid.view import notfound_view_config


@notfound_view_config(renderer='json', request_method='GET')
def notfound_view(request):
    request.response.status = 404
    return "Not found"
