
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

from .db import DeclBase
from .db import BaseMixin


class State(BaseMixin, DeclBase):
    code = Column(String, unique=True, nullable=False)
    name = Column(String, unique=False, nullable=False)

    def __repr__(self):
        return "{0} ({1})".format(self.name, self.code)


class Person(BaseMixin, DeclBase):
    first_name = Column(String, unique=False, nullable=False)
    last_name = Column(String, unique=False, nullable=True)

    @property
    def name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @property
    def cases(self):
        return [{'position': x.case_party.position,
                 'case': x.case_party.case[0],
                 'attorneys': [y.attorney for y in x.attorneys]}
                for x in self._cases]

    def __repr__(self):
        return self.name


class Attorney(Person):
    id = Column(Integer, ForeignKey('Person.id'), primary_key=True)
    bar_id = Column(String, unique=False, nullable=False)
    state_id = Column(Integer, ForeignKey('State.id'), nullable=False)

    state = relationship(
        "State", backref="attorneys",
        primaryjoin=(State.id == state_id)
    )

    @property
    def name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    __table_args__ = (
        UniqueConstraint('bar_id', 'state_id'),
    )

    @property
    def represents(self):
        return [{'position': x.person_case.case_party.position,
                 'person': x.person_case.person.name,
                 'case': x.person_case.case_party.case[0]}
                for x in self._represents]

    def __repr__(self):
        return "{0} {1}".format(self.state_id, self.name)


class CaseParty(BaseMixin, DeclBase):
    @property
    def is_defendant(self):
        return len(self.defendant_in) > 0

    @property
    def is_plaintiff(self):
        return len(self.plaintiff_in) > 0

    @property
    def position(self):
        if self.is_defendant:
            return 'defendant'
        elif self.is_plaintiff:
            return 'plaintiff'

    @property
    def case(self):
        if self.is_defendant:
            return self.defendant_in
        if self.is_plaintiff:
            return self.plaintiff_in


class PersonAssociation(BaseMixin, DeclBase):
    person_id = Column(Integer, ForeignKey('Person.id'),
                       unique=False, nullable=False)
    person = relationship(
        "Person", backref="_cases",
        primaryjoin=(Person.id == person_id)
    )

    case_party_id = Column(Integer, ForeignKey('CaseParty.id'),
                           unique=False, nullable=False)
    case_party = relationship(
        "CaseParty", backref="persons",
        primaryjoin=(CaseParty.id == case_party_id)
    )

    @property
    def attorneys(self):
        return [x.attorney for x in self._attorneys]


class AttorneyAssociation(BaseMixin, DeclBase):
    attorney_id = Column(Integer, ForeignKey('Attorney.id'),
                         unique=False, nullable=False)
    attorney = relationship(
        "Attorney", backref="_represents",
        primaryjoin=(Attorney.id == attorney_id)
    )

    person_case_id = Column(Integer, ForeignKey('PersonAssociation.id'),
                            unique=False, nullable=False)
    person_case = relationship(
        "PersonAssociation", backref="_attorneys",
        primaryjoin=(PersonAssociation.id == person_case_id)
    )


class Case(BaseMixin, DeclBase):
    case_number = Column(String, unique=False, nullable=False)
    title = Column(String, unique=False, nullable=True)
    state_id = Column(Integer, ForeignKey('State.id'), nullable=False)

    state = relationship(
        "State", backref="cases",
        primaryjoin=(State.id == state_id)
    )

    plaintiff_id = Column(Integer, ForeignKey('CaseParty.id'), nullable=False)
    plaintiff = relationship(
        "CaseParty", backref="plaintiff_in",
        primaryjoin=(CaseParty.id == plaintiff_id)
    )

    defendant_id = Column(Integer, ForeignKey('CaseParty.id'), nullable=False)
    defendant = relationship(
        "CaseParty", backref="defendant_in",
        primaryjoin=(CaseParty.id == defendant_id)
    )

    __table_args__ = (
        UniqueConstraint('case_number', 'state_id'),
    )
