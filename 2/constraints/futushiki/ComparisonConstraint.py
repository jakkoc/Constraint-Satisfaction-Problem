from typing import Dict, Tuple

from constraints.Constraint import Constraint


class ComparisonConstraint(Constraint[Tuple[int, int], int]):
    def __init__(self, smaller, bigger):
        super().__init__([smaller, bigger])
        self.smaller = smaller
        self.bigger = bigger

    def is_satisfied(self, assignment: Dict[Tuple[int, int], int]):
        if self.smaller not in assignment or self.bigger not in assignment:
            return True

        return assignment[self.smaller] < assignment[self.bigger]
