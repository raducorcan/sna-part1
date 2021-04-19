from dataclasses import dataclass
from typing import List, Dict


@dataclass
class RawInitiator:
    name: str
    href: str

    def to_dict(self):
        return {'name': self.name, 'href': self.href}

    @staticmethod
    def from_dict(kwargs):
        return RawInitiator(**kwargs)


@dataclass
class RawLawProject:
    id: str
    description: str
    initiators: Dict[str, List[RawInitiator]]
    senators_date: str
    deputies_date: str

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'initiators': {k: list(map(RawInitiator.to_dict, v)) for k, v in self.initiators.items()},
            'senators_date': self.senators_date,
            'deputies_date': self.deputies_date
        }

    @staticmethod
    def from_dict(kwargs: dict):
        initiators = {k: list(map(RawInitiator.from_dict, v)) for k, v in kwargs['initiators'].items()}
        kwargs.pop('initiators')
        return RawLawProject(**kwargs, initiators=initiators)
