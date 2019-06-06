from abc import ABCMeta, abstractmethod


class BaseCard(metaclass=ABCMeta):
    @property
    @abstractmethod
    def value(self):
        return NotImplementedError

    @value.setter
    @abstractmethod
    def value(self, val):
        return NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        return NotImplementedError


class ClassicCard(BaseCard):
    def __init__(self, rank, suit, value):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return (
            self.rank == other.rank
            and self.suit == other.suit
            and self.value == other.value
        )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def __repr__(self):
        return f"{self.rank} {self.suit} (value {self.value})"
