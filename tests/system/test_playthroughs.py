"""
These playthroughs behave as high-level integration tests. They test whether specific
cards behave and interact as intended.
"""

from pytest import raises
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.sequence import Sequence
from mtg_mana_simulator.repository import Repository

def test_playthrough1():
    """
    Test whether it's possible to play multiple lands due to Azusa, Lost but Seeking
    """
    azusa = Repository['Azusa, Lost but Seeking']
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
    phyrexian_arena = Repository['Phyrexian Arena']
    context = Context(hand=[ phyrexian_arena ], deck=[Card.filler]*5)
    context.mana_sequence = Sequence.once(3)

    context.new_turn()
    context.play_card("hand", 0) # Play Phyrexian Arena
    assert len(context.zones["hand"]) == 1
    context.new_turn()
    assert len(context.zones["hand"]) == 3
    context.new_turn()
    assert len(context.zones["hand"]) == 5

def playthrough3():
    """
    Test whether Crucible of Worlds allows playing lands from the graveyard
    """
    crucible_of_worlds = Repository['Crucible of Worlds']
    context = Context(hand=[ crucible_of_worlds ],
                      deck=[Card.filler]*3,
                      graveyard=[Card.untapped_land]*3)
    context.mana_sequence = Sequence.once(3)

    for _ in range(3):
        context.new_turn()
        assert context.zones["graveyard"][0].is_playable(context)
        context.play_card("graveyard", 0) # Play land from the graveyard
