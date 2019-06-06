from abc import ABCMeta, abstractmethod

from card.card import ClassicCard


class DeckBuilder(metaclass=ABCMeta):
    @abstractmethod
    def build(self):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def max_cards_count(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def name(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def card_class(cls):
        return NotImplementedError

    @abstractmethod
    def is_suitable_card(self, card):
        return NotImplementedError

    def get_name(self):
        return self.name


class ClassicDeckBuilder(DeckBuilder):
    card_class = ClassicCard
    jokers = [ClassicCard("JKR", "Red", 20), ClassicCard("JKR", "Black", 20)]
    suits = "spades diamonds clubs hearts".split()
    ranks = [str(i) for i in range(2, 11)] + list("JQKA")

    @property
    @classmethod
    @abstractmethod
    def joker(cls):
        return NotImplementedError

    def build(self):
        cards = []
        if self.joker:
            cards.extend(self.jokers)
        for suit in self.suits:
            for value, rank in enumerate(self.ranks):
                cards.append(self.card_class(rank, suit, value))
        return cards

    def is_suitable_card(self, card):
        return self._check_card_cls(card) and self._check_card_attrs_values(card)

    def _check_card_cls(self, card):
        return isinstance(card, self.card_class)

    def _check_card_attrs_values(self, card):
        return card.suit in self.suits and card.rank in self.ranks


class FrenchDeckBuilder(ClassicDeckBuilder):
    max_cards_count = 52
    joker = False
    name = "French deck (without jokers)"


class FrenchJokerDeckBuilder(FrenchDeckBuilder):
    max_cards_count = 54
    joker = True
    name = "French deck(with jokers)"


class ShortFrenchDeck(FrenchDeckBuilder):
    max_cards_count = 36
    joker = False
    name = "Short french deck"
    ranks = [str(i) for i in range(6, 11)] + list("JQKA")
