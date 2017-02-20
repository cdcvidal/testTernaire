from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

# TODO import package hash password

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    String,
    func,
    UniqueConstraint,

)

from .meta import Base

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    login = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    creation_date = Column(DateTime, server_default=func.now(),nullable=True)

    __table_args__ = (UniqueConstraint('login',  name='_login_uc'),
                 )

    def __init__(self, required , optional ):
        self.login = required['login']
        self.password = required['password']


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getCol():
       data = []
       for c in Users.__table__.columns :
           if c.name not in ['id']:
               data.append(c.name)
       return data

    def getColRequired():
       data = []
       for c in Users.__table__.columns :
           #print ( c.__dict__ )
           if c.name not in ['id','creation_date'] and not c.nullable:
               data.append(c.name)
       return data

    def getColOptional():
       data = []
       for c in Users.__table__.columns :
           #print ( c.__dict__ )
           if c.name not in ['id'] and c.nullable:
               data.append(c.name)
       return data

    def __repr__(self):
        return '<Users {}>'.format(self.login)
