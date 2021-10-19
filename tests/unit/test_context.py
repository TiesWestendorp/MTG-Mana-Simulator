"""
Unit tests for Context class
"""

from mtg_mana_simulator.context import Context

def test_discard_cards():
    """
    Test discard_cards instance method
    """
    for card_to_discard in range(7):
        context = Context(hand=list(range(7)))
        context.discard_cards([card_to_discard])
        assert context.zones["hand"] == [j for j in range(7) if j != card_to_discard]
