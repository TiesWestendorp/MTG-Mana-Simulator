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
    context = Context(hand=hand, mana=3)
    context.play_card(0) # Play Azusa
    for _ in range(3):
        assert context.zones["hand"][0].is_playable(context)
        context.play_card(0) # Play nth land
    assert not context.zones["hand"][0].is_playable(context)
    with raises(ValueError):
        context.play_card(0) # Can't play fourth land
