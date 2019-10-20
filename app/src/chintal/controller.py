

from .db import DeclBase
from .db import with_db


@with_db
def get_all(item_type=None, session=None):
    if not issubclass(item_type, DeclBase):
        raise Exception
    return session.query(item_type).all()


@with_db
def get_item(item_type=None, item_id=None, session=None):
    if not issubclass(item_type, DeclBase):
        raise Exception
    if not item_id:
        raise Exception
    return session.query(item_type).filter_by(id=item_id).one()
