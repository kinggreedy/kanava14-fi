"""init

Revision ID: 0e25dc05265d
Revises:
Create Date: 2020-09-27 18:42:17.784132

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0e25dc05265d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.Unicode(length=255), nullable=False),
        sa.Column('password', sa.Unicode(length=255), nullable=False),
        sa.Column('name', sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_index(
        'user_username_index',
        'users',
        ['username'],
        unique=True,
        mysql_length=255
    )
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Unicode(length=255), nullable=False),
        sa.Column('body', sa.UnicodeText(), nullable=True),
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('edited', sa.DateTime(), nullable=True),
        sa.Column('author', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['author'],
            ['users.id'],
            name=op.f('fk_posts_author_users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_posts')),
        sa.UniqueConstraint('title', name=op.f('uq_posts_title'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_index('user_username_index', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###