"""add workspace table

Revision ID: f023d91dddd8
Revises: 
Create Date: 2020-08-16 02:16:55.009140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f023d91dddd8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'workspace',
        sa.Column('id', sa.CHAR(32), unique=True, nullable=False),
        sa.Column('auto_increment', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('workspace')
