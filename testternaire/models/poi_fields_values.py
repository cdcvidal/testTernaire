from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref



from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    JSON,
    String,
)

from .meta import Base


class Association_PFV(Base):
    __tablename__ = 'association_pfv'
    pois_id = Column(Integer, ForeignKey('pois.id'), primary_key=True)
    fields_id = Column(Integer, ForeignKey('fields.id'), primary_key=True)
    values_id = Column(Integer, ForeignKey('values.id'), primary_key=True)

    pois = relationship("Pois", backref=backref("association_pfv", cascade="all, delete-orphan"))
    fields = relationship("Fields", backref=backref("association_pfv", cascade="all, delete-orphan"))
    values = relationship("Values", backref=backref("association_pfv", cascade="all, delete-orphan"))

    def __init__(self, pois=None, fields=None, values=None):
        self.pois = pois
        self.fields = fields
        self.values = values

    def __repr__(self):
        return '<Association_PFV {}>'.format(self.pois.name+" "+self.fields.name+" "+self.values.fieldValues)


class Pois(Base):
    __tablename__ = 'pois'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    fields = relationship(
    	'Fields',
    	secondary='association_pfv',
        viewonly=True
    )
    values = relationship(
    	'Values',
    	secondary='association_pfv',
        viewonly=True
    )

    def __init__(self, required , optional ):
        self.name = required['name']
        if 'values' in optional:
            self.values = optional['values']
        if 'fields' in optional:
            self.fields = required['fields']

    # def __init__(self, name):
    #     self.name = name
    #     self.fields=[]
    #     self.values=[]

    def __repr__(self):
        return '<Pois {}>'.format(self.name)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getCol():
       data = []
       for c in Pois.__table__.columns :
           if c.name not in ['id']:
               data.append(c.name)
       return data

    def getColRequired():
       data = []
       for c in Pois.__table__.columns :
           if c.name not in ['id','values','fields'] and not c.nullable:
               data.append(c.name)
       return data

    def getColOptional():
       data = []
       for c in Pois.__table__.columns :
           #print ( c.__dict__ )
           if c.name not in ['id'] and c.nullable:
               data.append(c.name)
       return data


class Fields(Base):
    __tablename__ = 'fields'
    id = Column(Integer, primary_key=True)
    pos = Column(Integer)
    name = Column(Text)

    pois = relationship(
    	'Pois',
    	secondary='association_pfv',
        viewonly=True
    )
    values = relationship(
    	'Values',
    	secondary='association_pfv',
        viewonly=True
    )

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.pois=[]
        self.values=[]

    def __repr__(self):
        return '<Fields {}>'.format(self.name+" "+str(self.pos))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getCol():
       data = []
       for c in Pois.__table__.columns :
           if c.name not in ['id']:
               data.append(c.name)
       return data

    def getColRequired():
       data = []
       for c in Pois.__table__.columns :
           if c.name not in ['id','values'] and not c.nullable:
               data.append(c.name)
       return data

    def getColOptional():
       data = []
       for c in Pois.__table__.columns :
           #print ( c.__dict__ )
           if c.name not in ['id'] and c.nullable:
               data.append(c.name)
       return data



class Values(Base):
    __tablename__ = 'values'
    id = Column(Integer, primary_key=True)
    fieldValues = Column(JSON)
    createdDate = Column(DateTime)
    status = Column(Text)

    fields = relationship(
    	Fields,
    	secondary='association_pfv',
    )
    pois = relationship(
    	'Pois',
    	secondary='association_pfv',
    )

    def __init__(self, fieldValues, createdDate, status):
        self.fieldValues = fieldValues
        self.createdDate = createdDate
        self.status = status
        self.fields=[]
        self.pois=[]

    def __repr__(self):
        return '<Values {}>'.format(self.fieldValues+" "+str(self.createdDate)+" "+self.status)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def getCol():
       data = []
       for c in Pois.__table__.columns :
           if c.name not in ['id']:
               data.append(c.name)
       return data

    def getColRequired():
       data = []
       for c in Pois.__table__.columns :
           if c.name not in ['id','values'] and not c.nullable:
               data.append(c.name)
       return data

    def getColOptional():
       data = []
       for c in Pois.__table__.columns :
           #print ( c.__dict__ )
           if c.name not in ['id'] and c.nullable:
               data.append(c.name)
       return data
