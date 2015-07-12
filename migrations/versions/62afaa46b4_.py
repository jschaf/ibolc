"""Create the inital table with some custom domains

Revision ID: 62afaa46b4
Revises: None
Create Date: 2015-07-05 22:19:38.392640

"""

# revision identifiers, used by Alembic.
revision = '62afaa46b4'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ibolc.database import Email, PhoneNumber, SSN, Zipcode

def upgrade():

    op.execute('create extension if not exists citext')
    op.execute('''
        create domain email as citext
        constraint email_ck_length
            check (char_length(value) between 3 and 255)
    ''')
    op.execute('''
        create domain phone_number as text
        constraint phone_number_ck_length
            check (char_length(value) between 7 and 25)
    ''')
    op.execute('''
        create domain zipcode as text
        constraint zipcode_ck_length_limit
            check (char_length(value) <= 10)
        constraint zipcode_ck_only_numeric_hyphens
            check(value ~ '^\d{5}([ \-]?\d{4})?$')
    ''')

    #TODO: install SSN type on heroku.
    op.execute('''
        create domain ssn as text
        constraint ssn_ck_length_limit
            check (char_length(value) <= 11)
        constraint ssn_ck_only_numeric_hyphens
            check(value ~ '^\d{3}-?\d{2}-?\d{4}$')
    ''')

    op.create_table('branch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('iso', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nice_name', sa.String(), nullable=False),
    sa.Column('iso3', sa.String(), nullable=True),
    sa.Column('num_code', sa.SmallInteger(), nullable=True),
    sa.Column('phone_code', sa.Numeric(precision=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=2), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address1', sa.String(), nullable=False),
    sa.Column('address2', sa.String(), nullable=True),
    sa.Column('address3', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('zipcode', Zipcode(), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['state.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('ssn', SSN(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('cell_phone', PhoneNumber(), nullable=True),
    sa.Column('email', Email(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('soldier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('branch_id', sa.Integer(), nullable=False),
    sa.Column('component', postgresql.ENUM('Active', 'National Guard', 'Reserve', name='mil_component'), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branch.id'], ),
    sa.ForeignKeyConstraint(['id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cadre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['soldier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['soldier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('student')
    op.drop_table('cadre')
    op.drop_table('soldier')
    op.drop_table('person')
    op.drop_table('roles')
    op.drop_table('address')
    op.drop_table('users')
    op.drop_table('state')
    op.drop_table('country')
    op.drop_table('branch')
    op.execute('drop domain if exists email')
    op.execute('drop domain if exists phone_nuber')
    op.execute('drop domain if exists zipcode')
