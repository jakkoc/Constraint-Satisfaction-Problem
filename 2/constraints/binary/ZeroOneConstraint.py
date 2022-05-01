from typing import List, Dict, Tuple

from constraints.Constraint import Constraint


class ZeroOneConstraint(Constraint[Tuple[int, int], int]):
    def __init__(self, variables: List[Tuple[int, int]]):
        super().__init__(variables)
        self.half_length = len(variables) // 2

    def is_satisfied(self, assignment: Dict[Tuple[int, int], int]):
        zeros = len([variable for variable in self.variables if variable in assignment and assignment[variable] == 0])
        ones = len([variable for variable in self.variables if variable in assignment and assignment[variable] == 1])

        return zeros <= self.half_length and ones <= self.half_length
