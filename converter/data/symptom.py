from dataclasses import dataclass
from typing import List

from data.base import EventData

from parsec import *
from converter.helpers import *


@dataclass(frozen=True)
class Symptom:
    name: str
    intensity: int
    duration: timedelta

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            name = yield until_delimiter()
            intensity = yield key_value("Intensity", number()) << maybe_more()
            duration = (
                yield optional(key_value("Duration", time_elapsed())) << maybe_more()
            )
            return Symptom(
                name=name,
                intensity=intensity,
                duration=duration,
            )

        return p

    @classmethod
    def parse(cls, data: str) -> "Symptom":
        return cls.Parser().parse(text=data)


@dataclass(frozen=True)
class SymptomData(EventData):
    symptoms: List[Symptom]

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            symptoms = yield many1(Symptom.Parser())
            notes = yield optional(event_notes())
            return SymptomData(symptoms=symptoms, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "SymptomData":
        return cls.Parser().parse(text=data)
