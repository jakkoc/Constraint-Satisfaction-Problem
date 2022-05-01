from constraints import Constraint
from typing import TypeVar, Dict, Callable

V = TypeVar('V')
D = TypeVar('D')


class UnaryConstraint(Constraint.Constraint[V, D]):
    def __init__(self, value: V, unary_predicate: Callable[[D], bool]):
        super().__init__([value])
        self.value = value
        self.unary_predicate = unary_predicate

    def is_satisfied(self, assignment: Dict[V, D]):
        if self.value not in assignment:
            return True

        return self.unary_predicate(assignment[self.value])
