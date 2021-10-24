from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Type

from data.base import EventData
from data.symptom import SymptomData
from data.bm import BowelMovementData

from parsec import *
from helpers import *


def notes_parser() -> Parser:
    @generate
    def p():
        notes = yield key_value("Notes", everything()) ^ everything().parsecapp(none)
        return notes

    return p


def timestamp_parser() -> Parser:
    @generate
    def p():
        month = yield number(2) << string("/")
        day = yield number(2) << string("/")
        year = yield number(4) << delimiter()
        hour = yield number(2) << string(":")
        minute = yield number(2)
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    return p


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
    def process(cls, data: List[str]) -> Optional["Event"]:
        timestamp = timestamp_parser().parse(data.pop(0))
        kind = data.pop(0)
        event_data_cls = cls.kind_to_subclass(kind)
        if not event_data_cls:
            return None
        data = event_data_cls.process(data=data)
        notes = notes_parser().parse(data.pop(-1)) if data else None
        return cls(timestamp=timestamp, kind=kind, data=data, notes=notes)
