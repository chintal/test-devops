

import os
import csv
import uuid
import random

from sqlalchemy.orm.exc import NoResultFound

from chintal.db import clear_database
from chintal.db import commit_metadata
from chintal.db import with_db
from chintal.models import Person
from chintal.models import Attorney
from chintal.models import Case
from chintal.models import State
from chintal.models import CaseParty
from chintal.models import PersonAssociation
from chintal.models import AttorneyAssociation

from chintal.controller import get_all


@with_db
def generate_states(session=None):
    with open(os.path.join('sample_data', 'states.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for name, abbrev in reader:
            try:
                _ = session.query(State).filter_by(
                    code=abbrev, name=name).one()
                continue
            except NoResultFound:
                pass
            state = State(code=abbrev, name=name)
            session.add(state)
            session.flush()


@with_db
def _get_states(session=None):
    return get_all(item_type=State, session=session)


def _get_names():
    fn, ln = [], []
    with open(os.path.join('sample_data', 'names.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for first_name, last_name in reader:
            fn.append(first_name), ln.append(last_name)
    return fn, ln


first_names, last_names = _get_names()


def _get_random_name():
    return random.choice(first_names), random.choice(last_names)


def _generate_attorneys():
    _rval = []
    for _ in range(1000):
        o = Attorney(first_name=random.choice(first_names),
                     last_name=random.choice(last_names),
                     bar_id=uuid.uuid4(),
                     state_id=random.choice(states).id)
        _rval.append(o)
    return _rval


def _generate_people():
    _rval = []
    for _ in range(5000):
        o = Person(first_name=random.choice(first_names),
                   last_name=random.choice(last_names))
        _rval.append(o)
    return _rval


def _choose_attorneys(state):
    na = random.randint(1, 2)
    candidates = [x for x in attorneys if x.state_id == state.id]
    return random.sample(candidates, na)


@with_db
def generate_cases(session=None):
    for _ in range(100):
        state = random.choice(states)

        npl = random.randint(1, 2)
        ndef = random.randint(1, 2)

        # This is a very dumb approach that will result in all manner
        # of absurdities.

        _people = random.sample(people, npl + ndef)
        _plaintiffs = _people[:npl]
        _defendants = _people[npl:]

        plaintiff = CaseParty()
        session.add(plaintiff)
        defendant = CaseParty()
        session.add(defendant)

        for person in _plaintiffs:
            session.add(person)
            pa = PersonAssociation(person=person, case_party=plaintiff)
            session.add(pa)

            _pattorneys = _choose_attorneys(state)
            for _attorney in _pattorneys:
                session.add(_attorney)
                aa = AttorneyAssociation(attorney=_attorney,
                                         person_case=pa)
                session.add(aa)

        for person in _defendants:
            session.add(person)
            pa = PersonAssociation(person=person, case_party=defendant)
            session.add(pa)

            _pattorneys = _choose_attorneys(state)
            for _attorney in _pattorneys:
                session.add(_attorney)
                aa = AttorneyAssociation(attorney=_attorney,
                                         person_case=pa)
                session.add(aa)

        if len(_plaintiffs) > 1:
            pm = ' et. al.'
        else:
            pm = ''

        if len(_defendants) > 1:
            dm = ' et. al.'
        else:
            dm = ''

        title = "{0}{1} v. {2}{3}".format(_plaintiffs[0].name, pm,
                                          _defendants[0].name, dm)
        case = Case(
            title=title,
            case_number=uuid.uuid4(),
            state_id=state.id,
            plaintiff=plaintiff,
            defendant=defendant,
        )
        # print("CASE", title)
        session.add(case)
        session.commit()
        session.flush()


if __name__ == '__main__':
    clear_database()
    commit_metadata()
    generate_states()
    states = _get_states()
    attorneys = _generate_attorneys()
    people = _generate_people()
    generate_cases()

