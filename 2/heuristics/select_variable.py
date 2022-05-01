from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, List, Set

V = TypeVar('V')
D = TypeVar('D')


class VariableSelector(Generic[V, D], ABC):
    @abstractmethod
    def select(self, unassigned: List[V], domains: Dict[V, Set[D]]):
        ...


class FirstVariableSelector(VariableSelector):
    def select(self, unassigned: List[V], domains: Dict[V, Set[D]]):
        return unassigned[0]


class MostConstrainedVariableSelector(VariableSelector):
    def select(self, unassigned: List[V], domains: Dict[V, Set[D]]):
        return min(unassigned, key=lambda v: len(domains[v]))