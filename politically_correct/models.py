import uuid

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy_utils.models import Timestamp
from sqlalchemy_utils.types import UUIDType

from .config import cfg

# SQLAlchemy configuration
Base = declarative_base()
engine = sa.create_engine(cfg.DATABASE_URL, convert_unicode=True)

# Apply sqlite driver hacks
if 'sqlite' in cfg.DATABASE_URL:
    @sa.event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    @sa.event.listens_for(engine, "begin")
    def do_begin(conn):
        # emit our own BEGIN
        conn.execute("BEGIN")

session = scoped_session(sessionmaker(bind=engine))


class Tweet(Base, Timestamp):
    """Tweet model."""

    __tablename__ = 'tweets'

    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    twitter_id = sa.Column(sa.BigInteger, unique=True, nullable=False)
    text = sa.Column(sa.Text, nullable=False)

    def __repr__(self):
        return ('<{cls}: {self.twitter_id} {self.text}>'
                .format(cls=self.__class__.__name__, self=self))


class Category(Base, Timestamp):
    """Category model."""

    __tablename__ = 'categories'
    id = sa.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    tag = sa.Column(sa.String(255), unique=True, index=True)
    name = sa.Column(sa.String(255))
    tweets = relationship(Tweet,
                          secondary=lambda: tweet_categories,
                          backref='categories')

    def __repr__(self):
        return ('<{cls}: {self.tag} {self.name}>'
                .format(cls=self.__class__.__name__, self=self))


tweet_categories = sa.Table(
    'tweets_categories',
    Base.metadata,
    sa.Column('c_id', UUIDType, sa.ForeignKey(Category.id), primary_key=True),
    sa.Column('t_id', UUIDType, sa.ForeignKey(Tweet.id), primary_key=True)
)


def create_tables():
    Base.metadata.create_all(engine)
