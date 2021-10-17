from dataclasses import dataclass
from typing import List

from data import EventData

from parsec import *
from helpers import *


def symptom_intensity():
    return (
        (string("Intensity:") >> spaces() >> many1(digit()))
        .parsecmap("".join)
        .parsecmap(int)
    )


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
            name = yield until_delimiter() << spaces()
            intensity = yield symptom_intensity() << delimiter() << spaces()
            duration = yield symptom_duration() ^ (
                empty() ^ (delimiter() + spaces())
            ).parsecmap(none)
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
            symptoms = yield many1(Symptom.Parser() << (delimiter() ^ string("")))
            notes = yield event_notes() ^ empty().parsecmap(none)
            return SymptomData(symptoms=symptoms, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "SymptomData":
        return cls.Parser().parse(text=data)
