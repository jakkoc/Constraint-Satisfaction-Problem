from typing import List, Dict, Tuple

from constraints.Constraint import Constraint


class TrinityConstraint(Constraint[Tuple[int, int], int]):
    def __init__(self, variables: List[Tuple[int, int]]):
        super().__init__(variables)

    def is_satisfied(self, assignment: Dict[Tuple[int, int], int]):
        for index in range(len(self.variables) - 2):
            if self.variables[index] not in assignment or self.variables[index + 1] not in assignment or self.variables[index + 2] not in assignment:
                continue
            if assignment[self.variables[index]] == assignment[self.variables[index + 1]] == assignment[self.variables[index + 2]]:
                return False
        return True
