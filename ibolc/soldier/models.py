from ibolc.database import (
    Column,
    ReferenceCol,
    relationship
)
from ibolc.person.models import Person

from sqlalchemy.dialects.postgresql import ENUM

mil_component_enum = ENUM('Active', 'National Guard', 'Reserve',
                          name='mil_component')


class Soldier(Person):
    __tablename__ = 'soldier'
    id = ReferenceCol('person', primary_key=True)
    branch_id = ReferenceCol('branch')
    branch = relationship('Branch')
    component = Column('component', mil_component_enum)

    __mapper_args__ = {
        'polymorphic_identity': 'soldier',
    }

    def __repr__(self):
        return "<Soldier({})>".format(self.last_name)
