from typing import Generic, TypeVar, Dict, Set
from abc import ABC, abstractmethod

V = TypeVar('V')
D = TypeVar('D')


class DomainErasure(Generic[V, D], ABC):
    @abstractmethod
    def erase(self, variable: V, value: D, assignments: Dict[V, D], domains: Dict[V, Set[D]]):
        ...
