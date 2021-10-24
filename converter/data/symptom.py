from dataclasses import dataclass
import functools
from typing import List, Tuple

from data.base import EventData

from parsec import *
from helpers import *


def intensity_parser() -> Parser:
    @generate
    def p():
        intensity = yield key_value("Intensity", number()) ^ (
            everything().parsecapp(none)
        )
        return intensity

    return p


def duration_parser() -> Parser:
    @generate
    def p():
        duration = yield key_value("Duration:", time_elapsed()) ^ (
            everything().parsecapp(none)
        )
        return duration

    return p


@dataclass(frozen=True)
class Symptom:
    name: str
    intensity: int
    duration: timedelta


@dataclass(frozen=True)
class SymptomData(EventData):
    symptoms: List[Symptom]

    @classmethod
    def process(cls, data: List[str]) -> "SymptomData":
        def build_symptoms(acc: Tuple[list, dict], x: str):
            result, partial = acc
            intensity = intensity_parser().parse(text=x)
            if intensity:
                partial["intensity"] = intensity
                return result, partial
            duration = duration_parser().parse(text=x)
            if duration:
                partial["duration"] = duration
            result.append(Symptom(**partial))
            partial = dict(name=x)
            return result, partial


        functools.reduce(build_symptoms, data[1:], ([], dict(name=data[0])))

        symptoms: List[Symptom] = []
        acc = dict()
        for col in data:
            updated = False
            if "name" not in acc:
                acc["name"] = col
                updated = True
            if not updated:
                intensity = intensity_parser().parse(text=col)
                if intensity:
                    acc["intensity"] = intensity
                    updated = True
            if not updated:
                duration = duration_parser().parse(text=col)
                if duration:
                    acc["duration"] = duration
                    updated = True
            symptoms.append(Symptom(**acc))
            acc = dict()
            updated = False
