"""
Unit tests for Actions methods
"""

import mtg_mana_simulator.actions as Actions
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.context import Context
from mtg_mana_simulator.sequence import Sequence

def test_basic_untapped_into_play():
    """
    Test basic_untapped_into_play method
    """

    deck = [
        Card.basic_land,
        Card.basic_land,
        Card.filler,
        Card.filler
    ]
    context = Context(deck=deck)
    assert context.mana == 0
    assert context.land == 0
    assert context.mana_sequence == Sequence.zero
    assert len(list(filter(lambda c: c.name == "Basic land", context.zones["deck"]))) == 2
    Actions.basic_untapped_into_play(context)
    assert context.mana == 1
    assert context.land == 0
    assert context.mana_sequence == Sequence.one
    assert len(list(filter(lambda c: c.name == "Basic land", context.zones["deck"]))) == 1

def test_basic_tapped_into_play():
    """
    Test basic_tapped_into_play method
    """

    deck = [
        Card.basic_land,
        Card.basic_land,
        Card.filler,
        Card.filler
    ]
    context = Context(deck=deck)
    assert context.mana == 0
    assert context.land == 0
    assert context.mana_sequence == Sequence.zero
    assert len(list(filter(lambda c: c.name == "Basic land", context.zones["deck"]))) == 2
    Actions.basic_tapped_into_play(context)
    assert context.mana == 0
    assert context.land == 0
    assert context.mana_sequence == Sequence.one
    assert len(list(filter(lambda c: c.name == "Basic land", context.zones["deck"]))) == 1

def test_basic_to_hand():
    """
    Test test_basic_to_hand method
    """

    deck = [
        Card.basic_land,
        Card.basic_land,
        Card.filler,
        Card.filler
    ]
    context = Context(deck=deck)
    assert context.zones["hand"] == []
    assert len(list(filter(lambda c: c.name == "Basic land", context.zones["deck"]))) == 2
    Actions.basic_to_hand(context)
    assert context.zones["hand"] == [Card.basic_land]
    assert len(list(filter(lambda c: c.name == "Basic land", context.zones["deck"]))) == 1
