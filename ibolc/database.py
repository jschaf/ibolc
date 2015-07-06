# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""

from sqlalchemy import types
from sqlalchemy.dialects.postgresql.base import ischema_names
from sqlalchemy.orm import relationship

from ibolc.extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship


# pylint: disable=E1101
class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


# pylint: disable=R0903
class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
# pylint: disable=W0622,E1101
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, (str, bytes)) and id.isdigit(),
                isinstance(id, (int, float))),):
            return cls.query.get(int(id))
        return None


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)


# pylint: disable=W0232,R0201
class SSN(types.UserDefinedType):
    '''A row type for the SSN implementation for PostGres at
http://pgxn.org/dist/ssn/'''
    def get_col_spec(self):
        return 'SSN'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['ssn'] = SSN


class Zipcode(types.UserDefinedType):
    '''A row type for U.S. zipcodes.'''
    def get_col_spec(self):
        return 'zipcode'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['zipcode'] = Zipcode


class Email(types.UserDefinedType):
    '''A row type for email addresses.'''
    def get_col_spec(self):
        return 'email'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['email'] = Email


class PhoneNumber(types.UserDefinedType):

    def get_col_spec(self):
        return 'phone_number'

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process

ischema_names['phone_number'] = PhoneNumber
