import collections
from typing import List

from constraints.futushiki.ComparisonConstraint import ComparisonConstraint
from heuristics.select_value import OrderedValueSelector, RandomValueSelector
from heuristics.select_variable import MostConstrainedVariableSelector, FirstVariableSelector
from model.Binary import Binary
from model.Futoshiki import Futoshiki
from problem.ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from problem.forward_checking.BinaryDomainErasure import BinaryDomainErasure
from problem.forward_checking.FutoshikiDomainErasure import FutoshikiDomainErasure
from utils.DataReader import DataReader
from timeit import default_timer as timer
from matplotlib import pyplot as plt

backtracking_futoshiki_times = {}
backtracking_futoshiki_nodes = {}
backtracking_binary_times = {}
backtracking_binary_nodes = {}
forward_futoshiki_times = {}
forward_futoshiki_nodes = {}
forward_binary_times = {}
forward_binary_nodes = {}


def test_backtracking():
    data = DataReader.read('../data')

    for puzzle in data:
        if puzzle['type'] == 'binary':
            binary = Binary(puzzle)
            backtracking_csp = ConstraintSatisfactionProblem(binary.variables, binary.domains)
            start = timer()
            for constraint in binary.constraints:
                backtracking_csp.add_constraint(constraint)

            backtracking_csp.backtracking_search({})

            solutions = backtracking_csp.solutions

            if len(solutions) == 0:
                print(f"No solutions found for Binary {binary.rows} x {binary.columns}")
                continue

            end = timer()
            backtracking_binary_times[binary.rows] = round(end - start, 4)
            backtracking_binary_nodes[binary.rows] = backtracking_csp.visited_nodes

            print(f'Found {len(solutions)} solutions for Binary {binary.rows} x {binary.columns}')
            print(f"Visited nodes: {backtracking_csp.visited_nodes}")
            print(f"Time: {round(end - start, 4)} seconds")
            print("Sample result")

            sample = list(solutions[0].values())

            for index in range(len(sample)):
                print(sample[index], end=' ')

                if index % binary.rows == binary.rows - 1:
                    print()
        elif puzzle['type'] == 'futoshiki':
            futoshiki = Futoshiki(puzzle)
            start = timer()
            backtracking_csp = ConstraintSatisfactionProblem(futoshiki.variables, futoshiki.domains)

            for constraint in futoshiki.constraints:
                backtracking_csp.add_constraint(constraint)

            backtracking_csp.backtracking_search({})

            solutions = backtracking_csp.solutions

            end = timer()
            backtracking_futoshiki_times[futoshiki.rows] = round(end - start, 4)
            backtracking_futoshiki_nodes[futoshiki.rows] = backtracking_csp.visited_nodes

            if len(solutions) == 0:
                print(f"No solutions found for Futoshiki {futoshiki.rows} x {futoshiki.columns}")
                continue
            print(f"Visited nodes: {backtracking_csp.visited_nodes}")
            print(f"Time: {round(end - start, 4)} seconds")
            print(f'Found {len(solutions)} solutions for Futoshiki {futoshiki.rows} x {futoshiki.columns}')
            print("Sample result")

            sample = list(solutions[0].values())

            for index in range(len(sample)):
                print(sample[index], end=' ')

                if index % futoshiki.rows == futoshiki.rows - 1:
                    print()


def test_forward(heuristics=False, should_propagate: bool = False):
    data = DataReader.read('../data')

    for puzzle in data:
        if puzzle['type'] == 'binary':
            start = timer()
            binary = Binary(puzzle, False)

            forward_check_csp = ConstraintSatisfactionProblem(binary.variables, binary.domains)

            for constraint in binary.constraints:
                forward_check_csp.add_constraint(constraint)

            if heuristics:
                forward_check_csp.forward_checking({}, binary.domains,
                                                   BinaryDomainErasure(binary.rows, should_propagate),
                                                   MostConstrainedVariableSelector(), RandomValueSelector())
            else:
                forward_check_csp.forward_checking({}, binary.domains,
                                                   BinaryDomainErasure(binary.rows, should_propagate),
                                                   FirstVariableSelector(), OrderedValueSelector())

            solutions = forward_check_csp.solutions
            if len(solutions) == 0:
                print(f"No solutions found for Binary {binary.rows} x {binary.columns}")
                continue
            print(f"Visited nodes: {forward_check_csp.visited_nodes}")
            end = timer()
            forward_binary_times[binary.rows] = round(end - start, 4)
            forward_binary_nodes[binary.rows] = forward_check_csp.visited_nodes
            print(f"Time: {round(end - start, 4)} seconds")
            print(f'Found {len(solutions)} solutions for Binary {binary.rows} x {binary.columns}')
            print("Sample result")

            sample = list(solutions[0].values())

            for index in range(len(sample)):
                print(sample[index], end=' ')

                if index % binary.rows == binary.rows - 1:
                    print()
        elif puzzle['type'] == 'futoshiki':
            start = timer()
            futoshiki = Futoshiki(puzzle, True)

            forward_check_csp = ConstraintSatisfactionProblem(futoshiki.variables, futoshiki.domains)

            constraints = [(c.smaller, c.bigger) for c in futoshiki.constraints if type(c) == ComparisonConstraint]

            for constraint in futoshiki.constraints:
                forward_check_csp.add_constraint(constraint)

            if heuristics:
                forward_check_csp.forward_checking({}, futoshiki.domains,
                                                   FutoshikiDomainErasure(futoshiki.rows, constraints,
                                                                          should_propagate),
                                                   MostConstrainedVariableSelector(), RandomValueSelector())
            else:
                forward_check_csp.forward_checking({}, futoshiki.domains,
                                                   FutoshikiDomainErasure(futoshiki.rows, constraints,
                                                                          should_propagate),
                                                   FirstVariableSelector(), OrderedValueSelector())

            solutions = forward_check_csp.solutions
            end = timer()
            forward_futoshiki_times[futoshiki.rows] = round(end - start, 4)
            forward_futoshiki_nodes[futoshiki.rows] = forward_check_csp.visited_nodes

            if len(solutions) == 0:
                print(f"No solutions found for Futoshiki {futoshiki.rows} x {futoshiki.columns}")
                continue
            print(f"Visited nodes: {forward_check_csp.visited_nodes}")
            print(f"Time: {round(end - start, 4)} seconds")
            print(f'Found {len(solutions)} solutions for Futoshiki {futoshiki.rows} x {futoshiki.columns}')
            print("Sample result")

            first_solution = solutions[0]

            for rows in range(futoshiki.rows):
                for columns in range(futoshiki.columns):
                    print(first_solution[(2 * rows, 2 * columns)], end=" ")
                print()


def draw_diagram(puzzle_size: List[int], forward: List[float], ylabel: str, title: str):
    plt.plot(puzzle_size, forward)
    plt.xlabel("Puzzle size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    # Backtracking
    # test_backtracking()

    # Forward checking with arc consistency and heuristics
    test_forward(True, True)

    # Forward checking with heuristics
    # test_forward(True)

    # Forward checking
    # test_forward()

    sorted_futoshiki_forward_times = collections.OrderedDict(sorted(forward_futoshiki_times.items()))
    sorted_binary_forward_times = collections.OrderedDict(sorted(forward_binary_times.items()))
    sorted_futoshiki_forward_nodes = collections.OrderedDict(sorted(forward_futoshiki_nodes.items()))
    sorted_binary_forward_nodes = collections.OrderedDict(sorted(forward_binary_nodes.items()))

    print(sorted_futoshiki_forward_times)
    print(sorted_binary_forward_times)
    print(sorted_futoshiki_forward_nodes)
    print(sorted_binary_forward_nodes)