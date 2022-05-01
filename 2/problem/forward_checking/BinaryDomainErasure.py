from typing import Tuple, List

from problem.forward_checking.DomainErasure import *


class BinaryDomainErasure(DomainErasure[Tuple[int, int], int]):
    def __init__(self, size, should_propagate: bool = False):
        super().__init__()
        self._size = size
        self._should_propagate = should_propagate
        self._row_group_neighbours = self.__find_row_group_neighbours()
        self._column_group_neighbours = self.__find_column_group_neighbours()
        self._trinity_neighbours = self.__find_trinity_neighbours()

    def __find_trinity_neighbours(self):
        trinity_neighbours: Dict[V, List[Tuple[V, V]]] = {}

        for row in range(self._size):
            for column in range(self._size):
                trinity_neighbours[(row, column)] = []

        for row in range(self._size):
            for column in range(self._size - 2):
                first = (row, column)
                second = (row, column + 1)
                third = (row, column + 2)

                trinity_neighbours[first].append((second, third))
                trinity_neighbours[second].append((first, third))
                trinity_neighbours[third].append((first, second))

                first = (column, row)
                second = (column + 1, row)
                third = (column + 2, row)

                trinity_neighbours[first].append((second, third))
                trinity_neighbours[second].append((first, third))
                trinity_neighbours[third].append((first, second))

        return trinity_neighbours

    def __find_row_group_neighbours(self):
        return {(row, column): [(row, neighbour_column) for neighbour_column in range(self._size) if
                                column != neighbour_column] for row in
                range(self._size) for column in range(self._size)}

    def __find_column_group_neighbours(self):
        return {(row, column): [(neighbour_row, column) for neighbour_row in range(self._size) if
                                row != neighbour_row] for row in
                range(self._size) for column in range(self._size)}

    def erase(self, variable: V, value: D, assignments: Dict[V, D], domains: Dict[V, Set[D]]):
        assignments[variable] = value

        row_count = len([neighbour for neighbour in self._row_group_neighbours[variable] if
                         neighbour in assignments and assignments[neighbour] == value])
        column_count = len([neighbour for neighbour in self._column_group_neighbours[variable] if
                            neighbour in assignments and assignments[neighbour] == value])

        if row_count + 1 == self._size // 2:
            for neighbour in self._row_group_neighbours[variable]:
                if value in domains[neighbour]:
                    domains[neighbour].remove(value)
                    if not domains[neighbour] and neighbour not in assignments:
                        return False

        if column_count + 1 == self._size // 2:
            for neighbour in self._column_group_neighbours[variable]:
                if value in domains[neighbour]:
                    domains[neighbour].remove(value)
                    if not domains[neighbour] and neighbour not in assignments:
                        return False

        for neighbour in self._trinity_neighbours[variable]:
            first = neighbour[0]
            second = neighbour[1]

            if first in assignments and assignments[first] == value:
                if value in domains[second]:
                    domains[second].remove(value)
                    if not domains[second] and second not in assignments:
                        return False
                    continue

            if second in assignments and assignments[second] == value:
                if value in domains[first]:
                    domains[first].remove(value)
                    if not domains[first] and first not in assignments:
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
