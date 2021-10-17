import pytest

from datetime import datetime, timedelta

from parsec import *
from converter.helpers import *


def test_date_and_time():
    @generate
    def p():
        result = yield date_and_time()
        return result

    assert p.parse("12/21/2021, 11:30") == datetime(year=2021, month=12, day=21, hour=11, minute=30)


def test_time_elapsed():
    @generate
    def p():
        result = yield time_elapsed()
        return result
    
    assert p.parse("21:45") == timedelta(hours=21, minutes=45)


def test_optional_some():
    @generate
    def p():
        result = yield optional(string("hello world"))
        return result

    assert p.parse("hello world") == "hello world"


def test_optional_none():
    @generate
    def p():
        result = yield optional(string("hello world"))
        return result

    assert p.parse("") == None
