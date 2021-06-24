"""Add note and list tables to db

Revision ID: e1460b389d64
Revises: f36a688d91db
Create Date: 2021-06-24 10:45:26.196619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1460b389d64'
down_revision = 'f36a688d91db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('folder_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('shared', sa.Boolean(), nullable=False),
    sa.Column('type', sa.Enum('TEXT', 'LIST', name='notetype'), nullable=False),
    sa.Column('text_body', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['folder_id'], ['folder.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('folder_id', 'name', name='unique_folder_id_name')
    )
    op.create_table('list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('note_id', sa.Integer(), nullable=True),
    sa.Column('text_body', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('list')
    op.drop_table('note')
    # ### end Alembic commands ###
