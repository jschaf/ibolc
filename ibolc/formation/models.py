from ibolc.database import Column, db, ReferenceCol, relationship, SurrogatePK


class Formation(db.Model, SurrogatePK):
    __tablename__ = 'formation'

    name = Column(db.String, nullable=False)
    office_code = Column(db.String, nullable=False)
    uic = Column(db.String, nullable=False)

    soldiers = relationship('SoldierFormationJoin', backref='formation')

    def __repr__(self):
        return "<Formation({})>".format(self.name)


class SoldierFormationJoin(db.Model, SurrogatePK):
    __tablename__ = 'soldier_formation_join'

    formation_id = ReferenceCol('formation')
    soldier_id = ReferenceCol('soldier')

    start_date = Column(db.Date)
    end_date = Column(db.Date)

    def __repr__(self):
        return "<SoldierFormationJoin({}, {})>".format(self.soldier_id,
                                                       self.formation_id)

