from dataclasses import dataclass
from typing import List

from data.base import EventData

from parsec import *
from converter.helpers import *


def symptom_intensity():
    return string("Intensity:") >> spaces() >> number()


def symptom_duration():
    return string("Duration:") >> spaces() >> duration()


@dataclass(frozen=True)
class Symptom:
    name: str
    intensity: int
    duration: int

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            name = yield until_delimiter()
            intensity = yield symptom_intensity() << maybe_more()
            duration = yield optional(symptom_duration()) << maybe_more()
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
            symptoms = yield many1(Symptom.Parser() << optional(delimiter()))
            notes = yield optional(event_notes())
            return SymptomData(symptoms=symptoms, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "SymptomData":
        return cls.Parser().parse(text=data)
