from deck.exceptions import (
    UniquenessDeckException,
    UnsuitableCardException,
    FullDeckException,
    MultipleAddingException,
)


class DeckValidator:
    def __call__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        if not self.instance:
            raise ValueError
        self.multiple = kwargs.get("multiple", None)


class MultipleValidator(DeckValidator):
    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        cards = kwargs.get("cards", None)
        if self.multiple:
            if not isinstance(cards, list):
                raise MultipleAddingException(
                    "Awaiting list when set multiple flag")
        else:
            if isinstance(cards, list):
                raise MultipleAddingException(
                    "Set flag multiple=True to " "add list of cards")


class UniquenessValidator(DeckValidator):
    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        cards = kwargs.get("cards", None)
        if self.instance.is_unique:
            if isinstance(cards, list):
                if any([c in self.instance.cards for c in cards]):
                    raise UniquenessDeckException("Card is already in deck")
            elif cards in self.instance.cards:
                raise UniquenessDeckException("Card is already in deck")


class SuitableCardValidator(DeckValidator):
    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        cards = kwargs.get("cards", None)
        if isinstance(cards, list):
            if not all([self.instance.is_suitable_card(c) for c in cards]):
                raise UnsuitableCardException("Bad card tried")
        elif not self.instance.is_suitable_card(cards):
            raise UnsuitableCardException("Bad card tried")


class OverflowValidator(DeckValidator):
    def __call__(self, *args, **kwargs):
        super().__call__(*args, **kwargs)
        if self.instance.is_full and not self.instance.allow_overflow:
            raise FullDeckException("The deck is full")
