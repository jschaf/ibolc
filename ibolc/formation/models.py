from ibolc.database import Column, db, ReferenceCol, relationship, SurrogatePK
from ibolc.soldier.models import Soldier


class Formation(Soldier, SurrogatePK):
    __tablename__ = 'formation'

    name = Column(db.String, nullable=False)
    office_code = Column(db.String, nullable=False)
    uic = column(db.String, nullable=False)

    soldiers = relationship('SoldierFormationJoin', backref='formation')

    def __repr__(self):
        return "<Formation({})>".format(self.name)


class SoldierFormationJoin(Model, SurrogatePK):
    __tablename__ = 'SoldierFormationJoin'

    formation_id = ReferenceCol('formation')
    soldier_id = ReferenceCol('soldier')

    start_date = Column(db.Date)
    end_date = Column(db.Date)

