from ibolc.database import (
    Column,
    db,
    Model
)


# pylint: disable=no-init
class Country(Model):
    __tablename__ = 'country'
    id = Column(db.Integer, primary_key=True)
    iso = Column(db.String, nullable=False)
    name = Column(db.String, nullable=False)
    nice_name = Column(db.String, nullable=False)
    iso3 = Column(db.String)
    num_code = Column(db.SmallInteger)
    phone_code = Column(db.Numeric(5))

    def __repr__(self):
        return "<Country({})>".format(self.name)
