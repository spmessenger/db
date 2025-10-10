from sqlalchemy import and_, false, or_, ColumnElement
from .utils import is_right_hand_clause_null


class cond_seq:
    def __init__(self, ignore_null_right_hand: bool = True):
        self._need_ignore_null_right_hand = ignore_null_right_hand
        self._and_clauses: list[ColumnElement] = []
        self._or_clauses: list[ColumnElement] = []

    def and_(self, clause) -> 'cond_seq':
        if self._need_ignore_null_right_hand and is_right_hand_clause_null(clause):
            return self
        self._and_clauses.append(clause)
        return self

    def or_(self, clause) -> 'cond_seq':
        if self._need_ignore_null_right_hand and is_right_hand_clause_null(clause):
            return self
        self._or_clauses.append(clause)
        return self

    @property
    def clauses(self) -> tuple[ColumnElement[bool], ColumnElement[bool]]:
        return self.and_clauses, self.or_clauses

    @property
    def and_clauses(self) -> ColumnElement:
        return and_(*self._and_clauses) if len(self._and_clauses) != 1 else self._and_clauses[0]

    @property
    def or_clauses(self) -> ColumnElement:
        return or_(*self._or_clauses) if len(self._or_clauses) != 1 else self._or_clauses[0]
