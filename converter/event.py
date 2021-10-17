from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Type

from symptom import SymptomData
from bm import BowelMovementData

from parsec import *
from helpers import *


@dataclass(frozen=True)
class EventData:
    notes: Optional[str]

    @staticmethod
    def kind_to_subclass(kind: str) -> Optional[Type["EventData"]]:
        return {
            "Symptom": SymptomData,
            "Bowel Movement": BowelMovementData,
        }.get(kind)

    @property
    @classmethod
    def Parser(cls) -> Parser:
        raise NotImplementedError()

    @classmethod
    def parse(cls, data: str) -> "EventData":
        raise NotImplementedError()


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    kind: str
    data: EventData

    @property
    @classmethod
    def Parser(cls: Type["Event"]) -> Parser:
        @generate
        def p():
            timestamp = yield date_and_time()
            kind = yield until_delimiter()
            event_data = yield until_end_of_line()
            event_data_cls = EventData.kind_to_subclass(kind)
            if not event_data_cls:
                return None
            data = event_data_cls.parse(data=event_data)
            return cls(timestamp=timestamp, kind=kind, data=data)

        return p

    @classmethod
    def parse(cls: Type["Event"], data: str) -> Optional["Event"]:
        return cls.parse(data)