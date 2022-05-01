from constraints.binary.TrinityConstraint import TrinityConstraint
from constraints.binary.UniquenessConstraint import UniquenessConstraint
from constraints.binary.ZeroOneConstraint import ZeroOneConstraint


class Binary:
    def __init__(self, properties, forward_checking: bool = False):
        self.rows = properties['rows']
        self.columns = properties['cols']
        self._data = properties['data'].replace('\n', '')
        self.variables = [(row, column) for row in range(0, self.rows) for column in range(0, self.columns)]
        self.domains = {position: [0, 1] for position in self.variables}
        self.constraints = []
        self.forward_checking = forward_checking
        self.__read_constraints()

    def __read_constraints(self):
        self.__read_unary_constraints()
        self.constraints.append(self.__read_uniqueness_constraint())

        if not self.forward_checking:
            self.constraints.extend(self.__read_trinity_row_constraint())
            self.constraints.extend(self.__read_trinity_column_constraint())
            self.constraints.extend(self.__read_zero_one_row_constraint())
            self.constraints.extend(self.__read_zero_one_column_constraint())

    def __read_unary_constraints(self):
        for i in range(len(self._data)):
            if self._data[i] != 'x':
                self.domains[self.variables[i]] = [int(self._data[i])]

    def __read_trinity_row_constraint(self):
        return [TrinityConstraint(self.variables[row * self.columns: (row + 1) * self.columns]) for row in
                range(self.rows)]

    def __read_trinity_column_constraint(self):
        trinity_column_constraints = []

        for i in range(self.columns):
            column = [variable for variable in self.variables if variable[1] == i]
            trinity_column_constraints.append(TrinityConstraint(column))
        return trinity_column_constraints

    def __read_zero_one_row_constraint(self):
        return [ZeroOneConstraint(self.variables[row * self.columns: (row + 1) * self.columns]) for row in
                range(self.rows)]

    def __read_zero_one_column_constraint(self):
        trinity_column_constraints = []

        for i in range(self.columns):
            column = [variable for variable in self.variables if variable[1] == i]
            trinity_column_constraints.append(ZeroOneConstraint(column))
        return trinity_column_constraints

    def __read_uniqueness_constraint(self):
        return UniquenessConstraint(self.variables, self.rows)

    def __str__(self):
        return f'rows: {self.rows} cols: {self.columns} data: {len(self._data)} domains: {self.domains}'
