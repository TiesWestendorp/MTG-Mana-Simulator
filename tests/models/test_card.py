"""
Unit tests for Card class
"""

from models.card import Card
from models.sequence import Sequence

def test_approximate_net_mana_sequence():
    """
    Test approximate_net_mana_sequence instance method
    """
    assert Card().approximate_net_mana_sequence() == Sequence.zero
    for gold,mana,cost in zip(range(4), range(4), range(4)):
        gold_sequence = Sequence.repeat(gold)
        mana_sequence = Sequence.repeat(mana)
        card = Card(gold_sequence=gold_sequence, mana_sequence=mana_sequence, cost=cost)
        assert card.approximate_net_mana_sequence() == Sequence([gold+mana-cost], [gold+mana])

def test_netgain():
    """
    Test netgain instance method
    """
    assert Card().netgain() == 0
    for gold,mana,cost in zip(range(4), range(4), range(4)):
        gold_sequence = Sequence.repeat(gold)
        mana_sequence = Sequence.repeat(mana)
        card = Card(gold_sequence=gold_sequence, mana_sequence=mana_sequence, cost=cost)
        assert card.netgain() == gold+mana-cost

def test_is_ramp():
    """
    Test is_ramp instance method
    """
    assert Card().is_ramp() is False
    assert Card(gold_sequence=Sequence.zero).is_ramp() is False
    assert Card(gold_sequence=Sequence.one).is_ramp() is True
    assert Card(gold_sequence=Sequence([0], [1])).is_ramp() is True
    assert Card(mana_sequence=Sequence.zero).is_ramp() is False
    assert Card(mana_sequence=Sequence.one).is_ramp() is True
    assert Card(mana_sequence=Sequence([0], [1])).is_ramp() is True

def test_is_draw():
    """
    Test is_draw instance method
    """
    assert Card().is_draw() is False
    assert Card(draw_sequence=Sequence.zero).is_draw() is False
    assert Card(draw_sequence=Sequence.one).is_draw() is True
    assert Card(draw_sequence=Sequence([0], [1])).is_draw() is True

def test_untapped_rock():
    """
    Test untapped_rock static method
    """
    for cost,mana in zip(range(4), range(4)):
        spell = Card.untapped_rock(cost, mana)
        assert spell.land is False
        assert spell.cost == cost
        assert spell.mana_sequence == Sequence.repeat(mana)
        assert spell.draw_sequence == Sequence.zero
        assert spell.gold_sequence == Sequence.zero
        assert spell.lands_removed == 0

def test_tapped_rock():
    """
    Test tapped_rock static method
    """
    for cost,mana in zip(range(4), range(4)):
        spell = Card.tapped_rock(cost, mana)
        assert spell.land is False
        assert spell.cost == cost
        assert spell.mana_sequence == Sequence.repeat(mana).prefixed_by([0])
        assert spell.draw_sequence == Sequence.zero
        assert spell.gold_sequence == Sequence.zero
        assert spell.lands_removed == 0

def test_draw_spell():
    """
    Test draw_spell static method
    """
    for cost,mana in zip(range(4), range(4)):
        spell = Card.draw_spell(cost, mana)
        assert spell.land is False
        assert spell.cost == cost
        assert spell.mana_sequence == Sequence.zero
        assert spell.draw_sequence == Sequence.once(mana)
        assert spell.gold_sequence == Sequence.zero
        assert spell.lands_removed == 0

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
