from dataclasses import dataclass
from typing import Optional, Type

from parsec import *
from converter.helpers import *


@dataclass(frozen=True)
class EventData:
    notes: Optional[str]

    @classmethod
    def Parser(cls) -> Parser:
        raise NotImplementedError()

    @classmethod
    def parse(cls, data: str) -> Type["EventData"]:
        raise NotImplementedError()
