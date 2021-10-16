"""
These sanity checks behave as high-level integration tests. They test statistical
properties that the system as a whole should exhibit.
"""

from random import seed
from mtg_mana_simulator.ai import AI
from mtg_mana_simulator.card import Card
from mtg_mana_simulator.experiment import Experiment
from mtg_mana_simulator.metric import Metric

def test_sanity_check_1():
    """
    Sanity check #1: without ramp or draw, the sample of the probability of being
    on-curve is hypergeometrically distributed.
    """
    seed(1337)

    deck = 38*[Card.untapped_land] + 61*[Card.filler]
    ai = AI.naive

    experiment = Experiment(deck=deck, ai=ai, turns=8, repeats=500)
    results = list(experiment.evaluate([Metric.on_curve]).values())[0]

    # Population: 99, Sample size: 7+n,  Successes in population: 38, Successes in Sample: n
    hypergeometric = [0.983,0.925,0.819,0.676,0.519,0.372,0.250,0.158]

    for sample,exact in zip(results, hypergeometric):
        assert abs(sample - exact) < 0.05

def test_sanity_check_2():
    """
    Sanity check #2: by the pigeon-hole principle, have 100% chance to be on-curve
    given (n-6) lands in a deck of size n.
    """
    for land_count in range(50, 100, 10):
        deck = land_count*[Card.untapped_land] + 6*[Card.filler]

        experiment = Experiment(deck=deck, ai=AI.naive, turns=8, repeats=1)
        results = list(experiment.evaluate([Metric.on_curve]).values())[0]

        for sample in results:
            assert sample == 1.0

def test_sanity_check_3():
    """
    Sanity check #3: replacing filler by ramp or card draw improves probability of
    being on-curve.
    """
    seed(1337)

    deck1 = 38*[Card.untapped_land] + 61*[Card.filler]
    deck2 = 38*[Card.untapped_land] + 51*[Card.filler] + 10*[Card.untapped_rock(2, 1)]
    experiment1 = Experiment(deck=deck1, ai=AI.naive, turns=8, repeats=100)
    experiment2 = Experiment(deck=deck2, ai=AI.naive, turns=8, repeats=100)

    results1 = list(experiment1.evaluate([Metric.on_curve]).values())[0]
    results2 = list(experiment2.evaluate([Metric.on_curve]).values())[0]

    for sample1,sample2 in zip(results1, results2):
        assert sample1 - sample2 <= 0.05

def test_sanity_check_4():
    """
    Sanity check #3: replacing filler by card draw improves probability of
    being on-curve.
    """
    seed(1337)

    deck1 = 38*[Card.untapped_land] + 61*[Card.filler]
    deck2 = 38*[Card.untapped_land] + 51*[Card.filler] + 10*[Card.cantrip]
    experiment1 = Experiment(deck=deck1, ai=AI.naive, turns=8, repeats=100)
    experiment2 = Experiment(deck=deck2, ai=AI.naive, turns=8, repeats=100)

    results1 = list(experiment1.evaluate([Metric.on_curve]).values())[0]
    results2 = list(experiment2.evaluate([Metric.on_curve]).values())[0]

    for sample1,sample2 in zip(results1, results2):
        assert sample1 - sample2 <= 0.05

def test_sanity_check_5():
    """
    Sanity check #4: removing lands from deck decreases chances of being on curve.
    """
    seed(1337)

    deck1 = 38*[Card.untapped_land] + 61*[Card.filler]
    deck2 = 30*[Card.untapped_land] + 69*[Card.filler]
    experiment1 = Experiment(deck=deck1, ai=AI.naive, turns=8, repeats=100)
    experiment2 = Experiment(deck=deck2, ai=AI.naive, turns=8, repeats=100)

    results1 = list(experiment1.evaluate([Metric.on_curve]).values())[0]
    results2 = list(experiment2.evaluate([Metric.on_curve]).values())[0]

    for sample1,sample2 in zip(results1, results2):
        assert sample1 - sample2 >= -0.05
