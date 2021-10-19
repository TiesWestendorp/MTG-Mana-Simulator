"""
These playthroughs behave as high-level integration tests. They test whether specific
cards behave and interact as intended.
"""

from pytest import raises
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.sequence import Sequence

def test_playthrough1():
    azusa = Card(land_sequence=Sequence.repeat(2))
    hand = [ azusa, *[Card.untapped_land]*4 ]
    context = Context(hand=hand, deck=[], mana=3)
    assert context.land == 1
    context.play_card(0) # Play Azusa

    context.play_card(0) # Play first land
    context.play_card(0) # Play second land
    context.play_card(0) # Play third land

    print("BLA")
    print(context.land)
    print(context.zones["hand"][0].is_playable(context))

    assert not context.zones["hand"][0].is_playable(context)
