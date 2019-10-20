
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer

from contextlib import contextmanager
import functools

DATABASE_HOST = os.environ.get('DATABASE_HOST', default='localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', default=5432)
DATABASE_USER = os.environ.get('DATABASE_USER', default='legalist')
DATABASE_PASS = os.environ.get('DATABASE_PASS', default='legalist')
DATABASE_DB = os.environ.get('DATABASE_DB', default='legalist')


def build_db_uri(
        dbhost=DATABASE_HOST,
        dbport=DATABASE_PORT,
        dbuser=DATABASE_USER,
        dbpass=DATABASE_PASS,
        dbname=DATABASE_DB):
    return 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        dbuser, dbpass, dbhost, dbport, dbname
    )


def init_db_engine():
    return create_engine(
        build_db_uri(DATABASE_HOST, DATABASE_PORT,
                     DATABASE_USER, DATABASE_PASS,
                     DATABASE_DB)
    )


engine = init_db_engine()
Session = sessionmaker(expire_on_commit=False)
Session.configure(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def with_db(func):
    @functools.wraps(func)
    def inner(*args, session=None, **kwargs):
        if session is None:
            with get_session() as s:
                return func(*args, session=s, **kwargs)
        else:
            return func(*args, session=session, **kwargs)
    return inner


DeclBase = declarative_base()


class BaseMixin(object):
    @declared_attr
    def __tablename__(self):
        return self.__name__

    id = Column(Integer, primary_key=True)


def get_metadata():
    from . import models
    return DeclBase.metadata


def commit_metadata():
    metadata.create_all(engine)


metadata = get_metadata()
commit_metadata()
