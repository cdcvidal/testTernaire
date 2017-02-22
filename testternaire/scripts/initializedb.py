import os
import sys
import transaction
from datetime import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Pois, Values, Fields, Association_PFV, Users


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        #test INSERT Users
        # requiredVal = {}
        # optionalVal = {}
        # requiredVal['login'] = 'toto'
        # requiredVal['password'] = '0000'
        # User1 = Users(requiredVal, optionalVal)
        # dbsession.add(User1)

        #test INSERT Pois
        requiredVal = {}
        optionalVal = {}
        requiredVal['tour_id'] = "34"
        firstValue=Values(fieldValues="{'url':'http://laaaalu'}", createdDate=datetime(2014, 3, 25), status='en cours')
        firstPoi = Pois(requiredVal, optionalVal)
        firstField=Fields(pos=3, name='Champ_photo')

        first_association = Association_PFV(firstPoi, firstField, firstValue)
        dbsession.add(first_association)
