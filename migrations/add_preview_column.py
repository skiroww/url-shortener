"""Add preview column to links table

Revision ID: add_preview_column
Revises: 
Create Date: 2024-03-22 14:44:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'add_preview_column'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('links', sa.Column('preview', JSON, nullable=True))

def downgrade():
    op.drop_column('links', 'preview') 