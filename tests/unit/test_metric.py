"""
Unit tests for Metric class
"""

from sys import version_info
from statistics import StatisticsError
from pytest import raises
from mtg_mana_simulator.metric import Metric
from mtg_mana_simulator.trace import Trace

def traces():
    """Example traces"""
    trace1 = Trace(3, max_mana=[1,2,3])
    trace2 = Trace(3, max_mana=[1,2,2])
    trace3 = Trace(3, max_mana=[0,0,1])
    trace4 = Trace(3, max_mana=[0,0,0])
    return [trace1, trace2, trace3, trace4]

def similar_lists(list1, list2, eps=1e-3):
    """Checks elementwise whether difference between two elements is at most some number"""
    return all(map(lambda pair: abs(pair[0]-pair[1])<eps, zip(list1, list2)))

def test_compute():
    """
    Test compute instance method
    """
    assert Metric.identity.compute(traces()) == [
        (1, [1,1,0,0]),
        (2, [2,2,0,0]),
        (3, [3,2,1,0])]
    assert similar_lists(Metric.mean("max_mana").compute(traces()),     [0.5, 1.0,  1.5])
    assert similar_lists(Metric.median("max_mana").compute(traces()),   [0, 1, 1])
    if [version_info[0], version_info[1]] < [3, 8]:
        with raises(StatisticsError):
            Metric.mode("max_mana").compute(traces())
    else:
        assert similar_lists(Metric.mode("max_mana").compute(traces()), [1, 2, 3])
    assert similar_lists(Metric.variance("max_mana").compute(traces()), [1/3, 1+1/3, 1+2/3])
    assert similar_lists(Metric.below_curve.compute(traces()),          [0.5, 0.5, 0.75])
    assert similar_lists(Metric.on_curve.compute(traces()),             [0.5, 0.5, 0.25])
    assert similar_lists(Metric.above_curve.compute(traces()),          [0.0, 0.0, 0.0])
    assert similar_lists(Metric.minimum("max_mana").compute(traces()), [0, 0, 0])
    assert similar_lists(Metric.maximum("max_mana").compute(traces()), [1, 2, 3])

def test_minimum():
    """
    Test minimum static method
    """
    for mana,probability in zip([1,2,3,4], [1.0,0.75,0.5,0.25]):
        metric = Metric.above_threshold("max_mana", mana)
        assert metric.name == f"≥{mana}"
        assert metric.measure == "max_mana"
        assert metric.func(None, [1,2,3,4]) == probability

def test_percentile():
    """
    Test percentile static method
    """
    for fraction,element in zip([0.25, 0.5, 0.75, 1.0], [1,2,3,4]):
        metric = Metric.percentile("max_mana", fraction)
        assert metric.name == f"{fraction}th percentile"
        assert metric.measure == "max_mana"
        assert metric.func(None, [1,2,3,4]) == element
