from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import List


class Status(Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    DENIED = 'DENIED'


@dataclass
class Initiator:
    mp: str
    name: str
    party: str

    def to_dict(self):
        return {'mp': self.mp, 'party': self.party, 'name': self.name}

    @staticmethod
    def from_dict(kwargs):
        return Initiator(**kwargs)


@dataclass
class LawProject:
    id: str
    description: str
    initiators: List[Initiator]
    senators_date: date
    deputies_date: date
    year: int
    status: Status

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'initiators': list(map(Initiator.to_dict, self.initiators)),
            'senators_date': self.senators_date.strftime('%Y-%m-%d') if self.senators_date is not None else None,
            'deputies_date': self.deputies_date.strftime('%Y-%m-%d') if self.deputies_date is not None else None,
            'status': self.status.value,
            'year': self.year
        }

    @staticmethod
    def from_dict(kwargs):
        initiators = list(map(Initiator.from_dict, kwargs.get('initiators', [])))
        status = Status[kwargs.get('status', 'PENDING')]
        senators_date = _get_date_from_string(kwargs.get('senators_date', ''))
        deputies_date = _get_date_from_string(kwargs.get('deputies_date', ''))

        kwargs.pop('initiators')
        kwargs.pop('status')
        kwargs.pop('senators_date')
        kwargs.pop('deputies_date')

        return LawProject(**kwargs,
                          initiators=initiators,
                          status=status,
                          deputies_date=deputies_date,
                          senators_date=senators_date)


def _get_date_from_string(text):
    if text is None:
        return None
    try:
        return datetime.strptime(text, '%Y-%m-%d').date()
    except Exception:
        return None
