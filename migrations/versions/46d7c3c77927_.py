"""empty message

Revision ID: 46d7c3c77927
Revises: 0c850de8b0be
Create Date: 2024-02-19 10:44:41.491135

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '46d7c3c77927'
down_revision = '0c850de8b0be'
branch_labels = None
depends_on = None

'''
(myproject) c:\projects\myproject>flask db migrate
__file__:C:\projects\myproject\config.py
BASE_DIR:C:\projects\myproject
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
Generating c:\projects\myproject\migrations\versions\46d7c3c77927_.py ...  done
'''

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###

'''
(myproject) c:\projects\myproject>flask db upgrade
'''

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
