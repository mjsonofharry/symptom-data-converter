from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple, Type
from parsec import *


def delimiter():
    """Parse the delimiter character."""
    return string(",") << spaces()


def not_delimiter():
    return regex(r"[^,]+")


def until_delimiter():
    """Parse text until the delimiter character."""
    return not_delimiter() << delimiter()


def end_of_string():
    """Parse the end of a string."""
    return regex(r"$")


def end_of_line():
    """Parse the end of a line."""
    return regex(r"[\n]")


def until_end_of_line():
    """Parse text the end of a line."""
    return regex(r"[^\n]+")


def number(digits: int):
    """Parse a positive integer with a fixed length."""
    return count(digit(), digits).parsecmap(lambda characters: int("".join(characters)))


def quoted():
    """Parse text between double-quotes."""
    return string('"') >> regex(r'[^\\"]+') << string('"')


def bracketed():
    """Parse text between square brackets."""
    return string("[") >> regex(r"[^\]]+") << string("]")


def notes():
    """Parse notes."""
    return string('"Notes:') >> spaces() >> regex(r'[^\\"]+') << string('"')


def delimited_sequence(p: Parser):
    """Parse a sequence of delimited parsers until the end of the string."""
    return many1(p << (delimiter() ^ end_of_string()))


def date_and_time():
    @generate
    def p():
        month = yield number(2) << string("/")
        day = yield number(2) << string("/")
        year = yield number(4) << delimiter()
        hour = yield number(2) << string(":")
        minute = yield number(2) << delimiter()
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    return p


@dataclass(frozen=True)
class EventData:
    notes: Optional[str]

    @staticmethod
    def kind_to_subclass(kind: str) -> Type["EventData"]:
        return {
            "Breakfast": MealData,
            "Lunch": MealData,
            "Dinner": MealData,
            "Snack": MealData,
            "Supplements": MealData,
            "Drink": MealData,
            "Symptom": SymptomData,
            "Bowel Movement": BowelMovementData,
            "Exercise": ExerciseData,
        }[kind]

    @classmethod
    def parse(cls, data: str) -> "EventData":
        raise NotImplementedError()


@dataclass(frozen=True)
class MealData(EventData):
    QuantityStr = str
    ingredients: List[Tuple[str, Optional[QuantityStr]]]

    @classmethod
    def parse(cls, data: str) -> "MealData":
        @generate
        def ingredient_with_quantity():
            _ingredient = yield quoted() << delimiter()
            _quantity = yield string('"') >> bracketed() << string('"')
            return (_ingredient, _quantity)

        @generate
        def ingredient_without_quantity():
            _ingredient = yield quoted()
            return (_ingredient, None)

        def ingredient():
            return ingredient_with_quantity ^ ingredient_without_quantity

        @generate
        def ingredients_with_notes():
            _ingredients = yield many1(ingredient() << delimiter())
            _notes = yield notes() << end_of_string()
            return (_ingredients, _notes)

        @generate
        def ingredients_without_notes():
            _ingredients = yield delimited_sequence(ingredient())
            return (_ingredients, None)

        @generate
        def p():
            ingredients, notes = (
                yield ingredients_with_notes ^ ingredients_without_notes
            )
            return cls(ingredients=ingredients, notes=notes)

        return p.parse(data)


@dataclass(frozen=True)
class SymptomData(EventData):
    IntensityInt = int
    DurationStr = str
    symptoms: List[Tuple[str, IntensityInt, DurationStr]]

    @classmethod
    def parse(cls, data: str) -> "SymptomData":
        def intensity():
            return string("Intensity:") >> spaces() >> many1(digit())

        def duration():
            return string("Duration:") >> spaces() >> not_delimiter()


@dataclass(frozen=True)
class BowelMovementData(EventData):
    pass


@dataclass(frozen=True)
class ExerciseData(EventData):
    exercises: List[str]

    @classmethod
    def parse(cls: Type["ExerciseData"], data: str) -> "ExerciseData":
        @generate
        def exercises_with_notes():
            _exercises = yield many1(quoted() << delimiter())
            _notes = yield notes() << end_of_string()
            return (_exercises, _notes)

        @generate
        def exercises_without_notes():
            _exercises = yield delimited_sequence(quoted())
            return (_exercises, None)

        @generate
        def p():
            _exercises, _notes = yield exercises_with_notes ^ exercises_without_notes
            return cls(exercises=_exercises, notes=_notes)

        return p.parse(data)


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    kind: str
    data: EventData

    @classmethod
    def parse(cls: Type["Event"], data: str) -> "Event":
        @generate
        def p():
            timestamp = yield date_and_time()
            kind = yield until_delimiter()
            event_data = yield until_end_of_line()
            event_data_cls = EventData.kind_to_subclass(kind)
            data = event_data_cls.parse(data=event_data)
            return cls(timestamp=timestamp, kind=kind, data=data)

        return p.parse(data)


if __name__ == "__main__":
    pass
