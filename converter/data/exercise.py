from dataclasses import dataclass
from typing import List

from data.base import EventData

from parsec import *
from helpers import *


def exercises_with_notes():
    @generate
    def p():
        exercises = yield many1(quoted() << delimiter())
        notes = yield event_notes() << end_of_string()
        return (exercises, notes)

    return p


def exercises_without_notes():
    @generate
    def p():
        exercises = yield delimited_sequence(quoted())
        return (exercises, None)

    return p


@dataclass(frozen=True)
class ExerciseData(EventData):
    exercises: List[str]

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            exercises, notes = yield exercises_with_notes() ^ exercises_without_notes()
            return cls(exercises=exercises, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "ExerciseData":
        return cls.Parser().parse(text=data)
