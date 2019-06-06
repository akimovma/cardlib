from deck import Deck
from card.card import ClassicCard
from deck.builders import FrenchJokerDeckBuilder, ShortFrenchDeck

deck = Deck(
    # deck_builder_cls=FrenchJokerDeckBuilder
)
deck.draw(count=3)
card = [ClassicCard("9", "spades", 111)]
# deck.show_deck()
deck.add_card(card)

deck.show_deck()
