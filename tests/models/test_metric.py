"""
Unit tests for Metric class
"""

from models.metric import Metric

def traces():
    trace1 = [1,2,3]
    trace2 = [1,2,2]
    trace3 = [0,0,1]
    trace4 = [0,0,0]
    return [trace1, trace2, trace3, trace4]

def test_compute():
    """
    Test compute instance method
    """
    assert Metric.identity.compute(traces()) == [
        (1, [1,1,0,0]),
        (2, [2,2,0,0]),
        (3, [3,2,1,0])]
    assert Metric.mean.compute(traces())        == [0.5, 1.0,  1.5]
    assert Metric.on_curve.compute(traces())    == [0.5, 0.5, 0.25]
    assert Metric.above_curve.compute(traces()) == [0.0, 0.0, 0.0]
    assert Metric.minimum.compute(traces())     == [0, 0, 0]
    assert Metric.maximum.compute(traces())     == [1, 2, 3]

def test_minimum_mana():
    """
    Test minimum_mana static method
    """
    pass

def test_percentile():
    """
    Test percentile static method
    """
    pass
