from dataclasses import dataclass
from typing import List, Type


@dataclass(frozen=True)
class EventData:
    _data: List[str]

    @classmethod
    def from_cols(cls, data: List[str]) -> Type["EventData"]:
        raise NotImplementedError()

    def to_dicts(self) -> List[dict]:
        raise NotImplementedError()
