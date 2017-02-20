import pyramid.httpexceptions as excpt
from pyramid.view import view_config
from ..models import DBSession, Base, Pois, Fields, Values

from pyramid.response import Response
from sqlalchemy import select, text, bindparam, delete, join, update, exc
from sqlalchemy.orm import joinedload


@view_config(route_name='pois', renderer='json', request_method='OPTIONS')
def getOptions(request):
    request.response.status_code = 200
    return None


@view_config(route_name='pois', renderer='json', request_method='GET')
def getAllPois(request):
    allPois = DBSession.query(Pois).all()
    data = []
    for poi in allPois:
        tmp = poi.as_dict()
        data.append(tmp)
    request.response.headers.update({'Access-Control-Expose-Headers': 'true'})
    request.response.headers.update(
        {'X-Total-Count': '' + str(len(allPois)) + ''})
    request.response.status_code = 200
    return data


@view_config(route_name='pois', renderer='json', request_method='POST')
def createPoi(request):
    print("route post ok")
    colRequired = Pois.getColRequired()
    colOptional = Pois.getColOptional()
    requiredVal = {}
    optionalVal = {}
    nbFind = 0
    nbToFind = len(colRequired)
    print(colRequired)
    print(request.POST['name'])
    for item in colRequired:
        if item in request.POST:
            print(item)
            requiredVal[item] = request.POST[item]
            nbFind += 1
    for item in colOptional:
        if item in request.POST:
            optionalVal[item] = request.POST[item]

    if nbFind == nbToFind:
        try:
            newPoi = Pois(requiredVal, optionalVal)
            DBSession.add(newPoi)
            DBSession.commit()
        except exc.IntegrityError as e:
            DBSession().rollback()
            newPoi = DBSession.query(Pois).with_entities(Pois.id).filter(
                Pois.name == request.POST['name']).first()
            request.response.status_code = 409
            return {'id': '' + str(newPoi.id) + ''}
        if newPoi.id:
            request.response.status_code = 201
            return {'id': '' + str(newPoi.id) + ''}
            # return excpt.HTTPCreated()
        else:
            request.response.status_code = 422
            return None
            # return excpt.HTTPUnprocessableEntity()
    else:
        request.response.status_code = 400
        return None
        # raise excpt.HTTPBadRequest()


@view_config(route_name='pois/id', renderer='json', request_method='GET')
def getPoi(request):
    id_ = request.matchdict['id']
    poiID = DBSession.query(Pois).get(id_)
    poi = DBSession.query(Pois, Fields, Values).join(
        Pois.fields, Pois.values).filter(Pois.id == id_).first()
    print('raw poi', poi)
    data= []
    if poi is not None :
        for item in poi:
            print('item',item.as_dict())
            data.append(item.as_dict())
            print(data)
        return data
    else :
        request.response.status_code = 404
        return None
