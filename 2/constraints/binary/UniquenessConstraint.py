from typing import List, Dict, Tuple

from constraints.Constraint import Constraint


class UniquenessConstraint(Constraint[Tuple[int, int], int]):
    def __init__(self, variables: List[Tuple[int, int]], size):
        super().__init__(variables)
        self._size = size

    def is_satisfied(self, assignment: Dict[Tuple[int, int], int]):
        completed_rows = []
        completed_columns = []

        for index in range(self._size):
            current_row = [assignment[position] for position in assignment.keys() if position[0] == index]
            current_column = [assignment[position] for position in assignment.keys() if position[0] == index]

            if len(current_row) == self._size:
                completed_rows.append(current_row)

            if len(current_column) == self._size:
                completed_columns.append(current_column)

        return len(completed_rows) == len(set(map(tuple, completed_rows))) and len(completed_columns) == len(set(map(tuple, completed_columns)))
