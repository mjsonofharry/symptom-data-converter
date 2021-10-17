from dataclasses import dataclass
from typing import List, Tuple, Optional

from data import EventData

from parsec import *
from helpers import *


def ingredient_with_quantity():
    @generate
    def p():
        ingredient = yield quoted() << delimiter()
        quantity = yield string('"') >> bracketed() << string('"')
        return (ingredient, quantity)
    return p


def ingredient_without_quantity():
    @generate
    def p():
        ingredient = yield quoted()
        return (ingredient, None)
    return p


def ingredient():
    return ingredient_with_quantity() ^ ingredient_without_quantity()


def ingredients_with_notes():
    @generate
    def p():
        ingredients = yield many1(ingredient() << delimiter())
        notes = yield event_notes() << end_of_string()
        return (ingredients, notes)
    return p


def ingredients_without_notes():
    @generate
    def p():
        ingredients = yield delimited_sequence(ingredient())
        return (ingredients, None)
    return p


@dataclass(frozen=True)
class MealData(EventData):
    ingredients: List[Tuple[str, Optional[str]]]

    @classmethod
    def Parser(cls) -> Parser:
        @generate
        def p():
            ingredients, notes = (
                yield ingredients_with_notes ^ ingredients_without_notes
            )
            return cls(ingredients=ingredients, notes=notes)

        return p

    @classmethod
    def parse(cls, data: str) -> "MealData":
        return cls.Parser().parse(text=data)
