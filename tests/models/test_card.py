"""
Unit tests for Card class
"""

from models.card import Card
from models.sequence import Sequence

def test_static_instances():
    """
    Test properties of static instances
    """
    assert Card.untapped_land.name == "Untapped land"
    assert Card.untapped_land.land is True
    assert Card.untapped_land.cost == 0
    assert Card.untapped_land.lands_removed == 0
    assert Card.untapped_land.mana_sequence == Sequence.one
    assert Card.untapped_land.gold_sequence == Sequence.zero
    assert Card.untapped_land.draw_sequence == Sequence.zero

    assert Card.tapped_land.name == "Tapped land"
    assert Card.tapped_land.land is True
    assert Card.tapped_land.cost == 0
    assert Card.tapped_land.lands_removed == 0
    assert Card.tapped_land.mana_sequence == Sequence([0], [1])
    assert Card.tapped_land.gold_sequence == Sequence.zero
    assert Card.tapped_land.draw_sequence == Sequence.zero

    assert Card.cantrip.land is False
    assert Card.cantrip.cost == 1
    assert Card.cantrip.lands_removed == 0
    assert Card.cantrip.mana_sequence == Sequence.zero
    assert Card.cantrip.gold_sequence == Sequence.zero
    assert Card.cantrip.draw_sequence == Sequence([1], [0])
