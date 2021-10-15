"""
Unit tests for Metric class
"""

from pytest import raises
from statistics import StatisticsError
from models.metric import Metric

def traces():
    trace1 = [1,2,3]
    trace2 = [1,2,2]
    trace3 = [0,0,1]
    trace4 = [0,0,0]
    return [trace1, trace2, trace3, trace4]

def similar_lists(list1, list2, eps=1e-3):
    return all(map(lambda pair: abs(pair[0]-pair[1])<eps, zip(list1, list2)))

def test_compute():
    """
    Test compute instance method
    """
    assert Metric.identity.compute(traces()) == [
        (1, [1,1,0,0]),
        (2, [2,2,0,0]),
        (3, [3,2,1,0])]
    assert similar_lists(Metric.mean.compute(traces()),        [0.5, 1.0,  1.5])
    assert similar_lists(Metric.median.compute(traces()),      [0, 1, 1])
    with raises(StatisticsError):
        Metric.mode.compute(traces())
    assert similar_lists(Metric.variance.compute(traces()),    [1/3, 1+1/3, 1+2/3])
    assert similar_lists(Metric.below_curve.compute(traces()), [0.5, 0.5, 0.75])
    assert similar_lists(Metric.on_curve.compute(traces()),    [0.5, 0.5, 0.25])
    assert similar_lists(Metric.above_curve.compute(traces()), [0.0, 0.0, 0.0])
    assert similar_lists(Metric.minimum.compute(traces()),     [0, 0, 0])
    assert similar_lists(Metric.maximum.compute(traces()),     [1, 2, 3])

def test_minimum_mana():
    """
    Test minimum_mana static method
    """
    for mana,probability in zip([1,2,3,4], [1.0,0.75,0.5,0.25]):
        metric = Metric.minimum_mana(mana)
        assert metric.name == f"≥{mana} mana"
        assert metric.func(None, [1,2,3,4]) == probability

def test_percentile():
    """
    Test percentile static method
    """
    for fraction,element in zip([0.25, 0.5, 0.75, 1.0], [1,2,3,4]):
        metric = Metric.percentile(fraction)
        assert metric.name == f"{fraction}th percentile"
        assert metric.func(None, [1,2,3,4]) == element
