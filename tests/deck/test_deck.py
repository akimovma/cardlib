import pytest

from cardeck.deck import Deck
from deck import builders


def test_deck_creation():
    deck = Deck()
    builder = builders.FrenchDeckBuilder()
    assert deck.name == builder.get_name()
