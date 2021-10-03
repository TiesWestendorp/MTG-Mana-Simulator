"""
Sanity check #2: by the pigeon-hole principle, have 100% chance to be on-curve
given (n-6) lands in a deck of size n.
"""

from models import AI, Card, Experiment, Metric

for n in range(50, 100, 10):
    deck = n*[Card.untapped_land] + 6*[Card.filler]
    experiment = Experiment(deck=deck, agent=AI.naive, turns=8, repeats=1)

    results = list(experiment.evaluate([Metric.on_curve]).values())[0]

    for x in results:
        assert x == 1.0
