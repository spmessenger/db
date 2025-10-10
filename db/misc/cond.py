from sqlalchemy import and_, or_, ColumnElement
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
    def clause(self) -> ColumnElement | ColumnElement[bool] | bool:
        """Returns a single combined clause for use in where()"""
        and_clause = and_(*self._and_clauses) if self._and_clauses else True
        or_clause = or_(*self._or_clauses) if self._or_clauses else False

        if self._and_clauses and self._or_clauses:
            return and_(and_clause, or_clause)
        elif self._and_clauses:
            return and_clause
        elif self._or_clauses:
            return or_clause
        else:
            return True  # No conditions

    # Remove the old clauses property or keep it for backward compatibility
    @property
    def clauses(self) -> tuple[ColumnElement[bool] | bool, ColumnElement[bool] | bool]:
        """Returns tuple of (and_clauses, or_clauses) - use .clause for where()"""
        return self.and_clauses, self.or_clauses

    @property
    def and_clauses(self) -> ColumnElement | bool:
        return and_(*self._and_clauses) if len(self._and_clauses) > 1 else self._and_clauses[0] if self._and_clauses else True

    @property
    def or_clauses(self) -> ColumnElement | bool:
        return or_(*self._or_clauses) if len(self._or_clauses) > 1 else self._or_clauses[0] if self._or_clauses else False
