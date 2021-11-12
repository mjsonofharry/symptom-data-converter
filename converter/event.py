from dataclasses import dataclass
import dataclasses
from datetime import datetime
from typing import List, Optional, Type

from data.base import EventData
from data.symptom import SymptomData
from data.bm import BowelMovementData
import helpers


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    kind: str
    data: Optional[EventData]
    notes: Optional[str]

    @staticmethod
    def kind_to_subclass(kind: str) -> Optional[Type["EventData"]]:
        return {
            "Symptom": SymptomData,
            "Bowel Movement": BowelMovementData,
        }.get(kind)

    @classmethod
    def from_cols(cls, data: List[str]) -> Optional["Event"]:
        date_string: str = data.pop(0)
        time_string: str = data.pop(0)
        timestamp: datetime = helpers.parse_timestamp(
            date_string=date_string, time_string=time_string
        )
        kind: str = data.pop(0)
        event_data_cls: Optional[Type[EventData]] = cls.kind_to_subclass(kind)
        if not event_data_cls:
            return None
        notes: Optional[str] = (
            data.pop(-1).split(":", 1)[1].strip()
            if data and data[-1].startswith("Notes:")
            else None
        )
        event_data = event_data_cls.from_cols(data=data)
        return cls(timestamp=timestamp, kind=kind, data=event_data, notes=notes)

    def to_json(self):
        pass