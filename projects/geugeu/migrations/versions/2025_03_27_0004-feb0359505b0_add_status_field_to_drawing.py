"""add status field to drawing

Revision ID: feb0359505b0
Revises: 9b811c5af312
Create Date: 2025-03-27 00:04:47.472064

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "feb0359505b0"
down_revision: Union[str, None] = "9b811c5af312"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add status column with default value 'DRAFT'
    op.add_column(
        "drawing",
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="DRAFT",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("drawing", "status")
