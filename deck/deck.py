import random

from .builders import FrenchDeckBuilder
from .constants import DrawFrom
from .validators import (
    UniquenessValidator,
    SuitableCardValidator,
    OverflowValidator,
    MultipleValidator,
)

from .exceptions import (
    EmptyDeckException,
    UniqueOverflowDeckException,
    IndexDeckException,
    UnsuitableCardException,
    NullBuilderDeckException,
)


class Deck:

    card_validators = [
        MultipleValidator(),
        SuitableCardValidator(),
        OverflowValidator(),
        UniquenessValidator(),
    ]

    def __init__(self, builder_cls=FrenchDeckBuilder, shuffle=False,
                 allow_overflow=False, is_unique=True):
        """
        Initialization of the Deck
        :param builder_cls: Builder class for Deck
        :param shuffle: Shuffle flag
        :param allow_overflow: Do we allow more cards then in full deck
        :param is_unique: Do we allow duplicates
        """
        if not builder_cls:
            raise NullBuilderDeckException("builder must be set")
        self.__builder = builder_cls()
        self.__cards = []
        self.name = self.__builder.get_name()

        if allow_overflow and is_unique:
            raise UniqueOverflowDeckException()
        self.is_unique = is_unique
        self.allow_overflow = allow_overflow
        self.build(shuffle)

    def __repr__(self):
        return f"{self.name} - left({self.cards_left()})"

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def __setitem__(self, key, card):
        if not self.is_suitable_card(card):
            raise UnsuitableCardException("Not suitable card.")
        self.cards[key] = card

    def __contains__(self, item):
        if self.is_suitable_card(item):
            return any([i == item for i in self.cards])
        raise UnsuitableCardException("Not suitable card.")

    @property
    def cards(self):
        return self.__cards

    @property
    def is_empty(self):
        return not self.cards_left()

    @property
    def is_full(self):
        return self.cards_left() == self.__builder.max_cards_count

    def build(self, shuffle=False):
        self.__cards = self.__builder.build()
        if shuffle:
            self.shuffle()

    def show_card(self, pos):
        """
        Show card at position
        :param pos: Position of card in deck
        :return: None
        :raises: IndexDeckException if invalid index
        """
        try:
            print(self.cards[pos])
        except IndexError:
            raise IndexDeckException("There is no card there")

    def show_deck(self):
        """
        Just print the deck
        :return:
        """
        for card in self.cards:
            print(card)

    def add_card(self, cards, multiple=False):
        """
        Add card(s) to the Deck
        :param cards: Card instance or list of Card instances
        :param multiple: multiple adding flag
        :return: None
        """
        self.validate_card(cards, multiple)

        if multiple and isinstance(cards, list):
            return self.cards.extend(cards)
        return self.cards.append(cards)

    def _get_draw_from_index(self, draw_from):
        """
        Method to return index where we draw a card
        :param draw_from: DrawFrom enum instance
        :return: int
        """
        if draw_from.value == draw_from.RANDOM:
            return random.randint(0, self.cards_left())
        if draw_from.value == draw_from.TOP:
            return self.cards_left()
        return 0

    def _draw(self, draw_from=DrawFrom.BOTTOM):
        """
        Draw card from the Deck
        :param draw_from: DrawFrom enum instance
        :return: Card instance
        :raises: EmptyDeckException
        """
        try:
            return self.cards.pop(self._get_draw_from_index(draw_from))
        except IndexError:
            raise EmptyDeckException("The deck is empty")

    def shuffle(self):
        """
        Shuffle cards in deck using random shuffle.
        """
        random.shuffle(self)

    def cards_left(self):
        """
        How many cards in the Deck
        :return: int
        """
        return len(self)

    def draw(self, count=1, shuffle_before=False, draw_from=DrawFrom.TOP):
        """
        Draw card from the Deck.
        :param count: How many cards to draw
        :param shuffle_before: Do we need to shuffle before draw
        :param draw_from: Draw from top, bottom or random
        :return: Card instance
        """
        if shuffle_before:
            self.shuffle()
        if count > 1:
            cards = [self._draw(draw_from) for i in range(count)]
            return cards
        return self._draw(draw_from)

    def is_suitable_card(self, card):
        """
        If card is suitable for this Deck instance
        :param card: Card instance
        :return: bool
        """
        return self.__builder.is_suitable_card(card)

    def validate_card(self, cards, multiple):
        """
        Validation method for adding cards.
        :param cards: Card instance or list of cards
        :param multiple: multiple flag
        :return: None
        :raises: errors from validators
        """
        return [v(instance=self, cards=cards, multiple=multiple)
                for v in self.card_validators]
