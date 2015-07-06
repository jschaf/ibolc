from ibolc.database import (
    Column,
    db,
    ReferenceCol
)
from ibolc.soldier.models import Soldier


class Cadre(Soldier):
    __tablename__ = 'cadre'

    id = ReferenceCol('soldier', primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cadre',
    }

    def __repr__(self):
        return "<Cadre({})>".format(self.last_name)
