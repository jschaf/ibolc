from ibolc.database import ReferenceCol
from ibolc.soldier.models import Soldier


class Student(Soldier):
    __tablename__ = 'student'

    id = ReferenceCol('soldier', primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __repr__(self):
        return "<Student({})>".format(self.last_name)
