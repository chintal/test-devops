

import os
from flask import Flask

from flask_restful import Resource
from flask_restful import Api
from flask_restful import abort
from flask_restful import marshal_with
from flask_caching import Cache
from sqlalchemy.orm.exc import NoResultFound

from .db import with_db
from .models import Person
from .models import Attorney
from .models import Case
from .controller import get_all
from .controller import get_item
from .marshallers import person_marshaller
from .marshallers import attorney_marshaller
from .marshallers import case_marshaller

config = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 600,
    # 'CACHE_OPTIONS': None,
    'CACHE_REDIS_HOST': os.environ.get('CACHE_REDIS_HOST', '127.0.0.1'),
    'CACHE_REDIS_PORT': os.environ.get('CACHE_REDIS_PORT', 6379),
    'CACHE_REDIS_PASSWORD': os.environ.get('CACHE_REDIS_PASSWORD', None),
}

app = Flask(__name__)
app.config.from_mapping(config)

api = Api(app)
cache = Cache(app)


class AllItems(Resource):
    _item_class = None

    @with_db
    def get(self, session=None):
        return get_all(item_type=self._item_class, session=session)


class AllAttorneys(AllItems):
    _item_class = Attorney

    @cache.cached()
    @with_db
    @marshal_with(attorney_marshaller)
    def get(self, session=None):
        return super(AllAttorneys, self).get(session=session)


class AllPersons(AllItems):
    _item_class = Person

    @cache.cached()
    @with_db
    @marshal_with(person_marshaller)
    def get(self, session=None):
        return super(AllPersons, self).get(session=session)


class AllCases(AllItems):
    _item_class = Case

    @cache.cached()
    @with_db
    @marshal_with(case_marshaller)
    def get(self, session=None):
        return super(AllCases, self).get(session=session)


api.add_resource(AllAttorneys, '/attorneys')
api.add_resource(AllPersons, '/persons')
api.add_resource(AllCases, '/cases')


class GetItem(Resource):
    _item_class = None

    @with_db
    def get(self, item_id=None, session=None):
        try:
            return get_item(item_type=self._item_class, item_id=item_id, session=session)
        except NoResultFound:
            abort(404, message="{0} with id {1} not found"
                               "".format(self._item_class.__name__, item_id))

    def __repr__(self):
        return self.__class__.__name__


class GetAttorney(GetItem):
    _item_class = Attorney

    @cache.cached()
    @with_db
    @marshal_with(attorney_marshaller)
    def get(self, item_id, session=None):
        return super(GetAttorney, self).get(item_id, session=session)


class GetPerson(GetItem):
    _item_class = Person

    @cache.cached()
    @with_db
    @marshal_with(person_marshaller)
    def get(self, item_id, session=None):
        return super(GetPerson, self).get(item_id, session=session)


class GetCase(GetItem):
    _item_class = Case

    @cache.cached()
    @with_db
    @marshal_with(case_marshaller)
    def get(self, item_id, session=None):
        return super(GetCase, self).get(item_id, session=session)


api.add_resource(GetAttorney, '/attorneys/<int:item_id>')
api.add_resource(GetPerson, '/persons/<int:item_id>')
api.add_resource(GetCase, '/cases/<int:item_id>')


def run():
    app.run(debug=True)


if __name__ == '__main__':
    run()
