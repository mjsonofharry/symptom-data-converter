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
    return string("") ^ end_of_string()


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


def time_elapsed():
    """Parse a duration in the format of "HH:MM"."""

    @generate
    def p():
        hours = yield number() << string(":")
        minutes = yield number()
        return timedelta(hours=hours, minutes=minutes)

    return p


none = lambda _: None


def optional(p: Parser):
    """Parse something if it exists or else yield none."""
    return p ^ empty().parsecmap(none)


def maybe_more():
    """Parse the next delimiter if it exists."""
    return optional(delimiter()).parsecmap(none)


def key_value(key: str, p: Parser):
    """Parse something in the format of KEY:VALUE."""
    return string(key) >> string(":") >> spaces() >> p


def event_notes():
    """Parse notes."""
    return string('"Notes:') >> spaces() >> regex(r'[^\\"]+') << string('"')


def row_end():
    return event_notes() ^ end_of_line() ^ end_of_string()


def until_row_end():
    return (many(regex(r'[^\\"]+')).parsecmap(",".join) + event_notes()).parsecmap(
        ",".join
    ) ^ until_end_of_line()


def everything():
    return many(any()).parsecapp("".join)
