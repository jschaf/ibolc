"""make mil_component a table

Revision ID: 17034142d9b
Revises: 62afaa46b4
Create Date: 2015-07-08 00:10:59.166926

"""

# revision identifiers, used by Alembic.
revision = '17034142d9b'
down_revision = '62afaa46b4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.drop_column('soldier', 'component')
    op.execute('drop type mil_component')
    op.create_table('mil_component',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('abbreviation', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('soldier',
                  sa.Column('mil_component_id', sa.Integer(), sa.ForeignKey('mil_component.id'), nullable=False))


def downgrade():
    op.drop_constraint('soldier_mil_component_id_fkey', 'soldier')
    op.drop_column('soldier', 'mil_component_id')
    op.drop_table('mil_component')
    op.add_column('soldier',
        sa.Column('component', postgresql.ENUM('Active', 'National Guard', 'Reserve', name='mil_component'), nullable=True)
    )
