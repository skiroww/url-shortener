"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-03-22 17:49:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create links table
    op.create_table(
        'links',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('short_code', sa.String(length=10), nullable=False),
        sa.Column('custom_alias', sa.String(length=50), nullable=True),
        sa.Column('original_url', sa.Text(), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('click_count', sa.Integer(), server_default='0', nullable=True),
        sa.Column('last_accessed', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('preview', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.UniqueConstraint('custom_alias'),
        sa.UniqueConstraint('short_code')
    )


def downgrade() -> None:
    op.drop_table('links')
    op.drop_table('users') 