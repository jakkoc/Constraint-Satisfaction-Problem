from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict, List

V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D], ABC):

    def __init__(self, variables: List[V]):
        self.variables = variables

    @abstractmethod
    def is_satisfied(self, assignment: Dict[V, D]):
        ...