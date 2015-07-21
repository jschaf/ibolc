from ibolc.database import Column, db, ReferenceCol, relationship, SurrogatePK


class Formation(db.Model, SurrogatePK):
    __tablename__ = 'formation'

    name = Column(db.String, nullable=False)
    office_code = Column(db.String, nullable=False)
    uic = Column(db.String, nullable=False)

    soldiers = relationship('Soldier',
                            secondary='soldier_formation',
                            viewonly=True)

    def __repr__(self):
        return "<Formation({})>".format(self.name)


class SoldierFormation(db.Model, SurrogatePK):
    __tablename__ = 'soldier_formation'

    formation_id = ReferenceCol('formation')
    soldier_id = ReferenceCol('soldier')

    soldier = relationship('Soldier')
    formation = relationship('Formation')

    start_date = Column(db.Date)
    end_date = Column(db.Date)

    def __repr__(self):
        return "<SoldierFormation({}, {})>".format(self.soldier_id,
                                                   self.formation_id)

