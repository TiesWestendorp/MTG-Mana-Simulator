"""
Unit tests for Sequence class
"""

from mtg_mana_simulator.sequence import Sequence

def test_normalize():
    """
    Test normalize instance method
    """
    sequence = Sequence([], [])

    sequence.prefix = [1]
    sequence.pattern = [1]
    sequence = sequence.normalize()
    assert sequence.prefix  == []
    assert sequence.pattern == [1]

    sequence.prefix = [0]
    sequence.pattern = [1, 0]
    sequence = sequence.normalize()
    assert sequence.prefix  == []
    assert sequence.pattern == [0, 1]

    sequence.prefix = []
    sequence.pattern = [1, 1]
    sequence = sequence.normalize()
    assert sequence.prefix  == []
    assert sequence.pattern == [1]

    sequence.prefix = []
    sequence.pattern = [1, 0, 1, 0]
    sequence = sequence.normalize()
    assert sequence.prefix  == []
    assert sequence.pattern == [1, 0]

def test___eq__():
    """
    Test __eq__ instance method
    """
    assert Sequence([], [1]) == Sequence([1], [1])
    assert Sequence([0], [1, 0]) == Sequence([], [0, 1])
    assert Sequence([], [1]) != Sequence([0], [1])
    assert Sequence([], [1, 0]) != Sequence([], [0, 1])

def test___add__():
    """
    Test __add__ instance method
    """
    assert Sequence([], [1]) + Sequence([], [2]) == Sequence([], [3])
    assert Sequence([1], [2]) + Sequence([], [3]) == Sequence([4], [5])
    assert Sequence([0], [1, 0]) + Sequence([], [1, 0]) == Sequence([], [1])

def test_prefixed_by():
    """
    Test prefixed_by instance method
    """
    sequence = Sequence([1], [1]).prefixed_by([1])
    assert sequence.prefix  == []
    assert sequence.pattern == [1]

    sequence = Sequence([1], [2]).prefixed_by([0])
    assert sequence.prefix  == [0, 1]
    assert sequence.pattern == [2]

def test_finite_prefix():
    """
    Test finite_prefix instance method
    """
    assert [1, 1, 1] == Sequence([], [1]).finite_prefix(3)
    assert [0, 1, 1] == Sequence([0], [1]).finite_prefix(3)
    assert [1, 2, 3, 4, 4] == Sequence([1, 2, 3], [4]).finite_prefix(5)
    assert [0, 1, 1, 1, 1] == Sequence([0], [1]).finite_prefix(5)

def test_generator():
    """
    Test generator instance method
    """
    generator = Sequence([1], [2, 3]).generator()
    assert generator.__next__() == 1
    assert generator.__next__() == 2
    assert generator.__next__() == 3
    assert generator.__next__() == 2
    assert generator.__next__() == 3

def test_once():
    """
    Test once static method
    """
    assert Sequence.once(0).prefix  == []
    assert Sequence.once(0).pattern == [0]
    assert Sequence.once(1).prefix  == [1]
    assert Sequence.once(1).pattern == [0]

def test_repeat():
    """
    Test repeat static method
    """
    assert Sequence.repeat(0).prefix  == []
    assert Sequence.repeat(0).pattern == [0]
    assert Sequence.repeat(1).prefix  == []
    assert Sequence.repeat(1).pattern == [1]

def test_static_instances():
    """
    Test properties of static instances
    """
    assert Sequence.zero.prefix  == []
    assert Sequence.zero.pattern == [0]
    assert Sequence.one.prefix  == []
    assert Sequence.one.pattern == [1]
