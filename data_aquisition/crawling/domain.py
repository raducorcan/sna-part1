from dataclasses import dataclass
from typing import List


@dataclass
class RawInitiator:
    name: str
    href: str

    def to_dict(self):
        return {'name': self.name, 'href': self.href}


@dataclass
class RawLawProject:
    id: str
    description: str
    initiators: List[RawInitiator]
    senators_date: str
    deputies_date: str

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'initiators': list(map(RawInitiator.to_dict, self.initiators)),
            'senators_date': self.senators_date,
            'deputies_date': self.deputies_date
        }
