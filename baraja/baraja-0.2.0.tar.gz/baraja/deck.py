"""baraja.deck

the deck module contains classes and functions for representing card decks.

"""
import random

from baraja import card
from baraja.exceptions import DeckException


class Deck(object):
    """a deck of cards

    This object is a stateful representation of a deck of cards.

    In all card sequences returned from a Deck, item [-1] is considered to be
    the top of that stack.

    """
    def __init__(self, sourcelist):
        """create a deck by passing in a list of card objects
        """
        self._discarded = []
        self._drawn = []
        self._undrawn = list(sourcelist)

    @property
    def discarded(self):
        """return a clone of the list of discarded cards"""
        return [c.clone() for c in self._discarded]

    @property
    def drawn(self):
        """return a clone of the list of drawn cards"""
        return [c.clone() for c in self._drawn]

    @property
    def undrawn(self):
        """return a clone of the undrawn card list"""
        return [c.clone() for c in self._undrawn]

    def add(self, card):
        """add a card to the deck

        Insert a new card into the deck, it will be added to the bottom of
        the undrawn cards. Will raise a DeckException if the unique card
        id already exists in the deck.
        """
        if len([c for c in self._undrawn if c.uuid == card.uuid]) > 0:
            raise DeckException(f'Duplicate card found in deck: {card}')
        self._undrawn.insert(0, card.clone())

    def discard(self, card):
        """discard a card from the drawn list

        Remove the specified card from the drawn list into the discarded
        listed. Discarded cards have the possibility of being shuffled
        back into the undrawn. Will raise a DeckException if the card
        does not exist in the drawn list.
        """
        if card.uuid not in [c.uuid for c in self.drawn]:
            raise DeckException(f'Card not found in drawn list: {card}')
        for i, c in enumerate(self._drawn):
            if c.uuid == card.uuid:
                self._discarded.append(c.clone())
                del self._drawn[i]

    def draw(self):
        """draw a card

        Pop a card from undrawn and push it to drawn, returning a clone of
        the card or None if the deck is empty.

        """
        try:
            c = self._undrawn.pop()
            self._drawn.append(c)
            return c.clone()
        except IndexError:
            return None

    def remove(self, card):
        """remove a card from the deck

        returns the card if found or None if not.
        """
        ret = None
        for i, c in enumerate(self._undrawn):
            if c.uuid == card.uuid:
                ret = c.clone()
                del self._undrawn[i]
        for i, c in enumerate(self._drawn):
            if c.uuid == card.uuid:
                ret = c.clone()
                del self._drawn[i]
        for i, c in enumerate(self._discarded):
            if c.uuid == card.uuid:
                ret = c.clone()
                del self._discarded[i]
        return ret

    def shuffle(self, discarded=True):
        """shuffle the undrawn and discarded cards together

        optionally ignore the discarded cardsby specifying `discarded=False`
        """
        if discarded:
            self._undrawn.extend(self._discarded)
            del self._discarded[:]
        random.shuffle(self._undrawn)


class PlayingCardDeck(Deck):
    """a french style deck

    This deck contains 52 cards in four suits with value 1 through 13 in each.
    With 1, 11, 12, and 13 representing Ace, Jack, Queen, and King
    repsectively.

    """
    def __init__(self):
        """create a deck of french style playing cards"""
        cardlist = []
        for suit in card.PlayingCard.SUITS:
            for value in range(1, 14):
                cardlist.append(card.PlayingCard(value, suit))
        super(PlayingCardDeck, self).__init__(sourcelist=cardlist)
