from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

import random

V = TypeVar('V')
D = TypeVar('D')


class ValueSelector(Generic[V, D], ABC):
    @abstractmethod
    def select(self, domain: List[D]):
        ...


class OrderedValueSelector(ValueSelector):
    def select(self, domain: List[D]):
        return domain


class RandomValueSelector(ValueSelector):
    def select(self, domain: List[D]):
        random.shuffle(domain)
        return domain
