from datetime import datetime
from decimal import Decimal
from urllib.parse import quote_plus
from sqlalchemy import engine_from_config, create_engine
from pyramid.config import Configurator
# from pyramid.request import Request, Response
from pyramid.renderers import JSON
# from pyramid.authentication import AuthTktAuthenticationPolicy
# from pyramid.authorization import ACLAuthorizationPolicy



from sqlalchemy_utils import database_exists,create_database

#from .controllers.security import SecurityRoot
from .models import (
    DBSession,
    Base,
    dbConfig,
    )
from .views import add_routes
from pyramid.events import NewRequest
import os,sys


# from .pyramid_jwtauth import (
#     JWTAuthenticationPolicy,
#     includeme
#     )

"""Json adapter for datetime objects."""
def datetime_adapter(obj, request):
    """Json adapter for datetime objects."""
    try:
        return obj.strftime ('%d/%m/%Y %H:%M:%S')
    except :
        return obj.strftime ('%d/%m/%Y')

def decimal_adapter(obj, request):
    """Json adapter for Decimal objects.
    """
    return float(obj)

def bytes_adapter(obj, request):
    return base64.b64encode(obj).decode()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # settings['sqlalchemy.url'] = settings['cn.dialect'] + quote_plus(settings['sqlalchemy.url'])
    # settings['sqlalchemy.url'] = settings['cn.dialect'] + quote_plus(settings['sqlalchemy.url'])
    engine = engine_from_config(settings, 'sqlalchemy.')
    print (engine.url)
    if not database_exists(engine.url) :
        print("la base n'existe pas")
        create_database(engine.url)
    else :
        print("la base existe")
    dbConfig['url'] = settings['sqlalchemy.url']

    # """ Creation repertoire pour photos """
    # dbConfig['bspipes'] = {}
    # dbConfig['bspipes']['folder'] = settings['bspipes.folder']
    #
    # if(os.path.exists(dbConfig['bspipes']['folder']) ):
    #     try :
    #         os.access( dbConfig['bspipes']['folder'], os.W_OK)
    #         print("folder : %s exist" %(dbConfig['bspipes']['folder']))
    #     except :
    #         print("app cant write in this directory ask your admin %s" %(dbConfig['bspipes']['folder']) )
    #         raise
    #         #declenché erreur
    # else:
    #     print ("folder %s doesn't exist we gonna try to create it" %(dbConfig['bspipes']['folder']))
    #     try:
    #         os.makedirs(dbConfig['bspipes']['folder'])
    #         print("folder created : %s" %(dbConfig['bspipes']['folder']))
    #     except OSError as exception:
    #         if exception.errno != errno.EEXIST:
    #             raise
    #
    # dbConfig['bspipes']['folderReports'] = settings['bspipes.folderReports']
    # if(os.path.exists(dbConfig['bspipes']['folderReports']) ):
    #     try :
    #         os.access( dbConfig['bspipes']['folderReports'], os.W_OK)
    #         print("folder : %s exist" %(dbConfig['bspipes']['folderReports']))
    #     except :
    #         print("app cant write in this directory ask your admin %s" %(dbConfig['bspipes']['folderReports']) )
    #         raise
    #         #declenché erreur
    # else:
    #     print ("folder %s doesn't exist we gonna try to create it" %(dbConfig['bspipes']['folderReports']))
    #     try:
    #         os.makedirs(dbConfig['bspipes']['folderReports'])
    #         print("folder created : %s" %(dbConfig['bspipes']['folderReports']))
    #     except OSError as exception:
    #         if exception.errno != errno.EEXIST:
    #             raise

    """ Configuration de la connexion à la BDD """
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    Base.metadata.reflect(views=True)

    """ Configuration du serveur pyramid"""
    print(settings)
    config = Configurator(settings=settings , autocommit=True)
    config.include('pyramid_chameleon')
    # Add renderer for datetime objects
    json_renderer = JSON()
    json_renderer.add_adapter(datetime, datetime_adapter)
    json_renderer.add_adapter(Decimal, decimal_adapter)
    json_renderer.add_adapter(bytes, bytes_adapter)
    config.add_renderer('json', json_renderer)

    # Set up authentication and authorization
    # config.set_authorization_policy(ACLAuthorizationPolicy())
    #Enable JWT authentification
    # config.include('pyramid_jwt')

    #config.set_jwt_authentication_policy('secret' , expiration='')

    # includeme(config)
    # config.set_jwt_authentication_policy('secret', http_header='Auth-Header-Secure' , expiration=3600)


    # Set the default permission level to 'read'
    # config.set_default_permission('read')
    config.include('pyramid_tm')
    # config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    add_routes(config)
    config.scan()
    print("init complete")
    return config.make_wsgi_app()

# from pyramid.config import Configurator
# from .views import add_routes
# from pyramid.renderers import JSON
#
#
# from sqlalchemy_utils import database_exists,create_database
#
# from .models import (
#     DBSession,
#     Base,
#     dbConfig,
#     )
#
# from .views import add_routes
#
# def main(global_config, **settings):
#     """ This function returns a Pyramid WSGI application.
#     """
#     config = Configurator(settings=settings)
#     # config.include('pyramid_jinja2')
#     config.include('.models')
#     add_routes(config)
#     config.scan()
#     return config.make_wsgi_app()
