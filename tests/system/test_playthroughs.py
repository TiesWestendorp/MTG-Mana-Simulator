"""
These playthroughs behave as high-level integration tests. They test whether specific
cards behave and interact as intended.
"""

from pytest import raises
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.sequence import Sequence

def test_playthrough1():
    """
    Test whether it's possible to play multiple lands due to Azusa, Lost but Seeking
    """
    azusa = Card(cost=3, land_sequence=Sequence.repeat(2))
    context = Context(hand=[ azusa, *[Card.untapped_land]*4 ])
    context.mana_sequence = Sequence.once(3)

    context.new_turn()
    context.play_card("hand", 0) # Play Azusa
    for _ in range(3):
        assert context.zones["hand"][0].is_playable(context)
        context.play_card("hand", 0) # Play nth land
    assert not context.zones["hand"][0].is_playable(context)
    with raises(ValueError):
        context.play_card("hand", 0) # Can't play fourth land

def test_playthrough2():
    """
    Test whether Phyrexian Arena actually gives multiple cards per turn
    """
    phyrexian_arena = Card(cost=3, draw_sequence=Sequence.one.prefixed_by([0]))
    context = Context(hand=[ phyrexian_arena ], deck=[Card.filler]*5)
    context.mana_sequence = Sequence.once(3)

    context.new_turn()
    context.play_card("hand", 0) # Play Phyrexian Arena

    assert len(context.zones["hand"]) == 1
    context.new_turn()
    assert len(context.zones["hand"]) == 3
    context.new_turn()
    assert len(context.zones["hand"]) == 5
