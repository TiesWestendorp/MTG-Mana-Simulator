"""
Unit tests for helper methods
"""

from mtg_mana_simulator.helpers import divisors, lcm, running_maximum

def test_divisors():
    """
    Test divisors helper method
    """
    assert divisors(7)  == [1, 7]
    assert divisors(9)  == [1, 3, 9]
    assert divisors(12) == [1, 2, 3, 4, 6, 12]

def test_lcm():
    """
    Test lcm helper method
    """
    assert lcm(3,   3)
    assert lcm(2,   2*2) == 2*2
    assert lcm(3*3, 3*4) == 3*3*4

def test_running_maximum():
    """
    Test convexify helper method
    """
    assert running_maximum([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert running_maximum([2, 1, 4, 3]) == [2, 2, 4, 4]
    assert running_maximum([4, 3, 2, 1]) == [4, 4, 4, 4]
