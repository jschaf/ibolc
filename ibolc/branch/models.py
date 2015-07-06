from ibolc.database import (
    Column,
    db,
    Model
)


class Branch(Model):
    __tablename__ = 'branch'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    full_name = Column(db.String, nullable=False)
    code = Column(db.String)

    def __repr__(self):
        return "<Branch({})>".format(self.code)

# TODO: add rank
