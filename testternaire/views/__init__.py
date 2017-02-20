from pyramid.httpexceptions import default_exceptionresponse_view, HTTPNotFound
from pyramid.interfaces import IRoutesMapper
from pyramid.view import view_config

def add_routes(config):
    config.add_route('home' , 'home')

    config.add_route('users' , 'users')
    config.add_route('users/id' , 'users/{id}')
    config.add_route('pois' , 'pois')
    config.add_route('pois/id','pois/{id}')

    pass
