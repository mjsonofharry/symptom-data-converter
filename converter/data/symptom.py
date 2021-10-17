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
            intensity = yield symptom_intensity()
            duration = yield (delimiter() << spaces() << symptom_duration()) ^ (
                end_of_string() ^ (delimiter() + spaces())
            ).parsecmap(lambda x: None)
            return Symptom(name=name, intensity=intensity, duration=duration)

        return p

    @classmethod
    def parse(cls, data: str) -> "Symptom":
        return cls.Parser().parse(text=data)


def symptoms_with_notes():
    @generate
    def p():
        symptom = yield many1(Symptom.Parser() << delimiter())
        notes = yield event_notes() << end_of_string()
        return (symptom, notes)

    return p


def symptoms_without_notes():
    @generate
    def p():
        symptoms = yield many1(Symptom.Parser())
        return (symptoms, None)

    return p


@dataclass(frozen=True)
class SymptomData(EventData):
    symptoms: List[Symptom]

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            symptoms, notes = yield symptoms_with_notes() ^ symptoms_without_notes()
            return SymptomData(symptoms=symptoms, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "SymptomData":
        return cls.Parser().parse(text=data)
