from dataclasses import dataclass
from typing import Optional, Type

from parsec import *
from helpers import *


@dataclass(frozen=True)
class EventData:
    notes: Optional[str]

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            _ = yield optional(many(until_delimiter()))
            notes = yield optional(event_notes())
            return cls(notes=notes)
        return p

    @classmethod
    def parse(cls, data: str) -> Type["EventData"]:
        return cls.Parser().parse(text=data)
