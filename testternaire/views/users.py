import pyramid.httpexceptions as exc
from pyramid.view import view_config
from ..models import DBSession,Base,Users
from pyramid.response import Response
from sqlalchemy import select,text,bindparam,delete,join,update,exc
from datetime import datetime
from sqlalchemy.orm import joinedload

@view_config(route_name='users',renderer='json',request_method='GET' )
def getAllUsers(request):
    allUser = DBSession.query(Users).all()
    data = []
    for user in allUser :
        tmp = user.as_dict()
        data.append(tmp)
    request.response.headers.update({'Access-Control-Expose-Headers' : 'true'})
    request.response.headers.update({ 'X-Total-Count' : ''+str(len(allUser))+''})
    request.response.status_code = 200
    return data

@view_config(route_name='users',renderer='json',request_method='POST' )
def createUser(request):
    colRequired = Users.getColRequired()
    colOptional = Users.getColOptional()
    requiredVal = {}
    optionalVal = {}
    nbFind = 0
    nbToFind = len(colRequired)
    for item in colRequired :
        if item in request.POST:
            print (item)
            requiredVal[item] = request.POST[item]
            nbFind +=1
    for item in colOptional:
        if item in request.POST:
            optionalVal[item] = request.POST[item]

    if nbFind == nbToFind:
        try:
            newUser = Users(requiredVal,optionalVal)
            DBSession.add(newUser)
            DBSession.commit()
        except exc.IntegrityError as e:
            DBSession().rollback()
            newUser = DBSession.query(Users).with_entities(Users.id).filter(Users.first_name == request.POST['first_name']).filter(Users.last_name == request.POST['last_name']).first()
            request.response.status_code = 409
            return {'id': ''+str(newUser.id)+''}
        if newUser.id :
            request.response.status_code = 201
            return {'id': ''+str(newUser.id)+''}
            # return excpt.HTTPCreated()
        else :
            request.response.status_code = 422
            return None
            # return excpt.HTTPUnprocessableEntity()
    else:
        request.response.status_code = 400
        return None
        # raise excpt.HTTPBadRequest()

@view_config(route_name='users/id',renderer='json',request_method='GET' )
def getUser(request):
    id_ = request.matchdict['id']
    user = DBSession.query(Users).get(id_)
    if user is not None :
        data = user.as_dict()
        request.response.status_code = 200
        return data
    else :
        request.response.status_code = 404
        return None
        # return exc.HTTPNotFound()

@view_config(route_name='users/id',renderer='json',request_method='PUT' )
def modifyUserComplete(request):
    id_ = request.matchdict['id']
    user = DBSession.query(Users).get(id_)
    if user is None:
        request.response.status_code = 404
        return None
        # raise exc.HTTPNotFound()
    else :
        colRequired = Users.getColRequired()
        colOptional = Users.getColOptional()
        requiredVal = {}
        optionalVal = {}
        nbFind = 0
        nbToFind = len(colRequired)
        for item in colRequired :
            if item in request.POST:
                setattr( user, item, request.POST[item] )
                nbFind +=1
        for item in colOptional:
            if item in request.POST:
                setattr( user, item, request.POST[item] )

        if nbFind == nbToFind:
            DBSession.commit()
            request.response.status_code = 204
            return None
        else:
            request.response.status_code = 400
            return None

@view_config(route_name='users/id',renderer='json',request_method='PATCH' )
def modifyUser(request):
    id_ = request.matchdict['id']
    user = DBSession.query(Users).get(id_)
    if user is None:
        request.response.status_code = 404
        return None
        # raise exc.HTTPNotFound()
    else :
        allCol = Users.getCol()
        flagPresent = False
        for col in allCol:
            if col in request.params:
                setattr( user, col, request.params[col] )
                flagPresent = True
        if flagPresent:
            DBSession.commit()
            request.response.status_code = 204
            return None
            # return exc.HTTPNoContent()
        else :
            request.response.status_code = 400
            return None
            # raise exc.HTTPBadRequest()


@view_config(route_name='users/id',renderer='json',request_method='DELETE' )
def deleteUser(request):
    id_ = request.matchdict['id']
    user = DBSession.query(Users).filter(Users.id == id_ ).delete(synchronize_session='evaluate')
    DBSession.commit()
    if user:
        request.response.status_code = 202
        return None
        # return exc.HTTPAccepted()
    else:
        request.response.status_code = 404
        return None
        # return exc.HTTPNotFound()
