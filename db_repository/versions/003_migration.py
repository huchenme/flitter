from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String),
    Column('full_name', String),
    Column('timestamp', DateTime),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('name', String(length=64)),
    Column('password', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['full_name'].drop()
    pre_meta.tables['user'].columns['timestamp'].drop()
    post_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['full_name'].create()
    pre_meta.tables['user'].columns['timestamp'].create()
    post_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['password'].drop()
