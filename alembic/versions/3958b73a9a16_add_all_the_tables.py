"""Add all the tables

Revision ID: 3958b73a9a16
Revises: 74f3b5ba2a44
Create Date: 2023-09-23 20:46:28.311196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3958b73a9a16'
down_revision: Union[str, None] = '74f3b5ba2a44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###