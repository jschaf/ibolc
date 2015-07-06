from ibolc.database import (
    Column,
    db,
    Email,
    Model,
    PhoneNumber,
    ReferenceCol,
    relationship,
    SSN,
    SurrogatePK,
    Zipcode
)


# pylint: disable=too-few-public-methods
class State(Model, SurrogatePK):
    __tablename__ = 'state'
    code = Column(db.String(2), nullable=False)
    name = Column(db.String, nullable=False)

    def __repr__(self):
        return "<State({})>".format(self.name)


class Address(Model, SurrogatePK):
    __tablename__ = 'address'
    address1 = Column(db.String, nullable=False)
    address2 = Column(db.String)
    address3 = Column(db.String)
    city = Column(db.String, nullable=False)
    state_id = ReferenceCol('state')
    zipcode = Column(Zipcode, nullable=False)
    state = relationship('State')

    def __repr__(self):
        return "<Address({}...)>".format(self.address1[:10])


class Person(Model, SurrogatePK):
    __tablename__ = 'person'
    first_name = Column(db.String, nullable=False)
    middle_name = Column(db.String)
    last_name = Column(db.String, nullable=False)
    ssn = Column(SSN, nullable=False)
    dob = Column(db.Date, nullable=False)
    country_id = ReferenceCol('country')
    country = relationship('Country')
    address_id = ReferenceCol('address')
    address = relationship('Address')
    cell_phone = Column(PhoneNumber)
    email = Column(Email, nullable=False)
    type = Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<Person({})>".format(self.last_name)
