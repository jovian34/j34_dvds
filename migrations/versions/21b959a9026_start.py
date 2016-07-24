"""start

Revision ID: 21b959a9026
Revises: None
Create Date: 2015-11-15 22:18:39.490478

"""

# revision identifiers, used by Alembic.
revision = '21b959a9026'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dvds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('binder', sa.String(length=50), nullable=True),
    sa.Column('page', sa.Integer(), nullable=True),
    sa.Column('sleeve', sa.Integer(), nullable=True),
    sa.Column('imdb_page', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dvd_tag',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('dvd_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['dvd_id'], ['dvds.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dvd_tag')
    op.drop_table('dvds')
    op.drop_table('user')
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_table('tag')
    ### end Alembic commands ###
