"""add event journal

Revision ID: 000000000000
Revises: fc13e5c6ad67
Create Date: 2026-05-12

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000000000000'
down_revision = 'f22b49cf5347'

branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'event_journal',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_description', sa.Text(), nullable=False),
        sa.Column('event_at', sa.DateTime(timezone=False), server_default=sa.text('(now())'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_event_journal_id', 'event_journal', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_event_journal_id', table_name='event_journal')
    op.drop_table('event_journal')

