import copy
from typing import Generic, TypeVar, Dict, List, Set

from constraints.Constraint import Constraint
from heuristics.select_value import ValueSelector
from heuristics.select_variable import VariableSelector
from problem.forward_checking.DomainErasure import DomainErasure

V = TypeVar('V')
D = TypeVar('D')


class ConstraintSatisfactionProblem(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, Set[D]]):
        self.variables: List[V] = variables
        self.domains: Dict[V, Set[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        self.solutions = []
        self.visited_nodes = 0
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise ValueError("Each variable should have a domain assigned to it")

    def add_constraint(self, constraint: Constraint[V, D]):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError("Such variable does not exist in domain")
            self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assignment: Dict[V, D]):
        for constraint in self.constraints[variable]:
            if not constraint.is_satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D]):
        if len(assignment) == len(self.variables):
            self.solutions.append(assignment)
            return

        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        to_be_assigned: V = unassigned[0]
        for value in self.domains[to_be_assigned]:
            local_assignment = assignment.copy()
            local_assignment[to_be_assigned] = value
            self.visited_nodes += 1
            if self.consistent(to_be_assigned, local_assignment):
                self.backtracking_search(local_assignment)

    def forward_checking(self, assignment: Dict[V, D], domains: Dict[V, Set[D]], domain_erasure: DomainErasure[V, D],
                         variable_selector: VariableSelector[V, D], value_selector: ValueSelector[V, D]):
        if len(assignment) == len(self.variables):
            self.solutions.append(assignment)
            return

        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        to_be_assigned: V = variable_selector.select(unassigned, domains)

        values = value_selector.select(list(domains[to_be_assigned]))

        for value in values:
            local_assignment = assignment.copy()
            local_assignment[to_be_assigned] = value
            self.visited_nodes += 1
            if self.consistent(to_be_assigned, local_assignment):

                domain_copy = copy.deepcopy(domains)

                if domain_erasure.erase(to_be_assigned, value, local_assignment, domain_copy):
                    if self.consistent(to_be_assigned, local_assignment):
                        self.forward_checking(local_assignment, domain_copy, domain_erasure, variable_selector,
                                            value_selector)
