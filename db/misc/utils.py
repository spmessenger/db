import datetime
from collections.abc import Sequence
from sqlalchemy.sql.elements import BindParameter, Null


def clear_tzinfo(dt: datetime.datetime | None):
    if dt is not None:
        return dt.replace(tzinfo=None)


def get_utc_now():
    return datetime.datetime.now(datetime.UTC)


def is_right_hand_clause_null(clause):
    flag = False
    if isinstance(clause.right, Null):
        flag = True
    elif isinstance(clause.right, BindParameter) and is_empty(clause.right.value):
        flag = True
    return flag


def is_empty(seq: Sequence) -> bool:
    if isinstance(seq, Sequence) and len(seq) == 0:
        return True
    return False


def errorless_pop(obj, key):
    try:
        return obj.pop(key)
    except (AttributeError, KeyError, TypeError):
        return None
