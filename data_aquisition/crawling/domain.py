from dataclasses import dataclass
from typing import List


@dataclass
class RawInitiator:
    name: str
    href: str


@dataclass
class RawLawProject:
    id: str
    description: str
    initiators: List[RawInitiator]
    date: str
