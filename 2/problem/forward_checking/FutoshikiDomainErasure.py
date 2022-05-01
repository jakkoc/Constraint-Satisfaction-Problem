from typing import Tuple

from problem.forward_checking.DomainErasure import *


class FutoshikiDomainErasure(DomainErasure[Tuple[int, int], int]):
    def __init__(self, size, constraints, should_propagate: bool = False):
        super().__init__()
        self._size = size
        self._constraints = constraints
        self._should_propagate = should_propagate

        self._inequality_neighbours = self.__find_inequality_neighbours()
        self._row_group_neighbours = self.__find_row_group_neighbours()
        self._column_group_neighbours = self.__find_column_group_neighbours()


    def __find_inequality_neighbours(self):
        constraint_neighbours = {}

        for neighbour in self._constraints:
            smaller = neighbour[0]
            bigger = neighbour[1]

            if smaller not in constraint_neighbours:
                constraint_neighbours[smaller] = [('<', bigger)]
            else:
                constraint_neighbours[smaller].append(('<', bigger))

            if bigger not in constraint_neighbours:
                constraint_neighbours[bigger] = [('>', smaller)]
            else:
                constraint_neighbours[bigger].append(('>', smaller))

        return constraint_neighbours

    def __find_row_group_neighbours(self):
        return {(2 * row, 2 * column): [(2 * row, 2 * neighbour_column) for neighbour_column in range(self._size) if
                                        column != neighbour_column] for row in
                range(self._size) for column in range(self._size)}

    def __find_column_group_neighbours(self):
        return {(2 * row, 2 * column): [(2 * neighbour_row, 2 * column) for neighbour_row in range(self._size) if
                                        row != neighbour_row]
                for row in
                range(self._size) for column in range(self._size)}

    def erase(self, variable: V, value: D, assignments: Dict[V, D], domains: Dict[V, Set[D]]):
        assignments[variable] = value

        for neighbour in self._row_group_neighbours[variable]:
            if value in domains[neighbour]:
                domains[neighbour].remove(value)
                if not domains[neighbour] and neighbour not in assignments:
                    return False

        for neighbour in self._column_group_neighbours[variable]:
            if value in domains[neighbour]:
                domains[neighbour].remove(value)
                if not domains[neighbour] and neighbour not in assignments:
                    return False

        if variable in self._inequality_neighbours:
            for constraint in self._inequality_neighbours[variable]:
                operator = constraint[0]
                neighbour = constraint[1]

                if operator == '<':
                    domains[neighbour] = {v for v in domains[neighbour] if v > value}
                else:
                    domains[neighbour] = {v for v in domains[neighbour] if v < value}

                if not domains[neighbour] and neighbour not in assignments:
                    return False

        if self._should_propagate:
            for neighbour in self._row_group_neighbours[variable]:
                if len(domains[neighbour]) == 1 and neighbour not in assignments:
                    if not self.erase(neighbour, next(iter(domains[neighbour])), assignments, domains):
                        return False
            for neighbour in self._column_group_neighbours[variable]:
                if len(domains[neighbour]) == 1 and neighbour not in assignments:
                    if not self.erase(neighbour, next(iter(domains[neighbour])), assignments, domains):
                        return False

        return True
