"""renamed class 'Notes' to 'Note' in note field in the User model

Revision ID: decff3712f52
Revises: c75ca617683f
Create Date: 2022-11-24 12:35:38.922712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'decff3712f52'
down_revision = 'c75ca617683f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
