class DeckException(Exception):
    pass


class NullBuilderDeckException(DeckException):
    pass


class IndexDeckException(DeckException):
    pass


class FullDeckException(IndexDeckException):
    pass


class EmptyDeckException(IndexDeckException):
    pass


class UnsuitableCardException(DeckException):
    pass


class UniqueOverflowDeckException(DeckException):
    def __init__(self, *args, **kwargs):
        self.message = "Deck can't be unique and allow overflow"


class UniquenessDeckException(DeckException):
    pass


class MultipleAddingException(DeckException):
    pass
