from ibolc.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)
from ibolc.person.models import Person


class MilComponent(Model, SurrogatePK):
    __tablename__ = 'mil_component'
    name = Column(db.String, nullable=False)
    abbreviation = Column(db.String, nullable=False)


class Soldier(Person):
    __tablename__ = 'soldier'
    id = ReferenceCol('person', primary_key=True)
    branch_id = ReferenceCol('branch')
    branch = relationship('Branch')
    mil_component_id = ReferenceCol('mil_component')
    mil_component = relationship('MilComponent')

    __mapper_args__ = {
        'polymorphic_identity': 'soldier',
    }

    def __repr__(self):
        return "<Soldier({})>".format(self.last_name)
