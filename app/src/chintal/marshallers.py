

import copy
from flask_restful import fields


base_person_marshaller = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String
}


base_attorney_marshaller = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'bar_id': fields.String,
    'state': fields.String
}


base_case_marshaller = {
    'case_number': fields.String,
    'title': fields.String,
    'state': fields.String,
}


person_case_marshaller = {
    'position': fields.String,
    'case': fields.Nested(base_case_marshaller),
    'attorneys': fields.Nested(base_attorney_marshaller)
}

person_marshaller = copy.copy(base_person_marshaller)
person_marshaller.update({
    'cases': fields.Nested(person_case_marshaller)
})


attorney_represents_marshaller = {
    'position': fields.String,
    'person': fields.String,
    'case': fields.Nested(base_case_marshaller),
}


attorney_marshaller = copy.copy(base_attorney_marshaller)
attorney_marshaller.update({
    'represents': fields.Nested(attorney_represents_marshaller)
})


case_person_marshaller = {
    'person': fields.Nested(base_person_marshaller),
    'attorneys': fields.Nested(base_attorney_marshaller),
}

case_party_marshaller = {
    'persons': fields.Nested(case_person_marshaller)
}

case_marshaller = copy.copy(base_case_marshaller)
case_marshaller.update({
    'plaintiff': fields.Nested(case_party_marshaller),
    'defendant': fields.Nested(case_party_marshaller),
})
