from constraints.futushiki.ComparisonConstraint import ComparisonConstraint
from constraints.futushiki.CompletenessConstraint import CompletenessConstraint


class Futoshiki:
    def __init__(self, properties, is_forward_check=False):
        self.rows = properties['rows']
        self.columns = properties['cols']
        self._data = (properties['data'] + '-').split('\n')
        self.variables = []
        self.domains = {}
        self.constraints = []
        self.__parse_input_data()

        if not is_forward_check:
            self.constraints.extend(self.__read_row_completeness_constraints())
            self.constraints.extend(self.__read_columns_completeness_constraints())

    def __parse_input_data(self):
        for row in range(2 * self.rows - 1):
            for column in range(len(self._data[row])):
                if not Futoshiki.__is_operand(self._data[row][column]):
                    variable = (row, column)

                    self.variables.append(variable)
                    self.domains[variable] = [i for i in range(1, self.rows + 1)]

                    if self._data[row][column] != 'x':
                        given_value = int(self._data[row][column])

                        self.domains[variable] = [given_value]
                elif row % 2 == 0:
                    if self._data[row][column] == '>':
                        bigger = (row, column - 1)
                        smaller = (row, column + 1)
                        self.constraints.append(ComparisonConstraint(smaller, bigger))
                    elif self._data[row][column] == '<':
                        bigger = (row, column + 1)
                        smaller = (row, column - 1)
                        self.constraints.append(ComparisonConstraint(smaller, bigger))
                else:
                    if self._data[row][column] == '>':
                        bigger = (row - 1, 2 * column)
                        smaller = (row + 1, 2 * column)
                        self.constraints.append(ComparisonConstraint(smaller, bigger))
                    elif self._data[row][column] == '<':
                        bigger = (row + 1, 2 * column)
                        smaller = (row - 1, 2 * column)
                        self.constraints.append(ComparisonConstraint(smaller, bigger))

    def __read_row_completeness_constraints(self):
        return [CompletenessConstraint([(2 * row, 2 * column) for column in range(self.columns)]) for row in range(self.rows)]

    def __read_columns_completeness_constraints(self):
        return [CompletenessConstraint([(2 * row, 2 * column) for row in range(self.rows)]) for column in range(self.columns)]

    @staticmethod
    def __is_operand(symbol):
        return symbol == '>' or symbol == '<' or symbol == '-'

    def __str__(self):
        return f'Rows: {self.rows} Columns: {self.columns} Data: {self._data}'
