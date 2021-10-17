from datetime import datetime, timedelta
from typing import Optional

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


def empty():
    """Parse empty string."""
    return string("") ^ end_of_string() ^ end_of_line()


def until_end_of_line():
    """Parse text the end of a line."""
    return regex(r"[^\n]+")


def number(digits: Optional[int] = None):
    """Parse a positive integer."""
    if not digits:
        return many1(digit()).parsecmap("".join).parsecmap(int)
    return count(digit(), digits).parsecmap("".join).parsecmap(int)


def quoted():
    """Parse text between double-quotes."""
    return string('"') >> regex(r'[^\\"]+') << string('"')


def bracketed():
    """Parse text between square brackets."""
    return string("[") >> regex(r"[^\]]+") << string("]")


def delimited_sequence(p: Parser):
    """Parse a sequence of delimited parsers until the end of the string."""
    return many1(p << (delimiter() ^ end_of_string()))


def date_and_time():
    """Parse a date and time in the format of "MM/DD/YYYY, HH:MM"."""

    @generate
    def p():
        month = yield number(2) << string("/")
        day = yield number(2) << string("/")
        year = yield number(4) << delimiter()
        hour = yield number(2) << string(":")
        minute = yield number(2) << optional(delimiter())
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    return p


def time_elapsed():
    """Parse a duration in the format of "HH:MM"."""

    @generate
    def p():
        hours = yield (number(2) ^ number(1)) << string(":")
        minutes = yield number(2)
        return timedelta(hours=hours, minutes=minutes)

    return p


none = lambda _: None


def optional(p: Parser):
    return p ^ empty().parsecmap(none)


def maybe_more():
    return optional(delimiter()).parsecmap(none)


def key_value(key: str, p: Parser):
    return string(key) >> string(":") >> spaces() >> p


def event_notes():
    """Parse notes."""
    return string('"Notes:') >> spaces() >> regex(r'[^\\"]+') << string('"')
