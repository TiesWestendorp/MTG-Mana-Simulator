"""
Sanity check #4: removing lands from deck decreases chances of being on curve.
"""

from random import seed
from models import AI, Card, Experiment, Metric

seed(1337)

deck1 = 38*[Card.untapped_land] + 61*[Card.filler]
deck2 = 30*[Card.untapped_land] + 69*[Card.filler]
experiment1 = Experiment(deck=deck1, agent=AI.naive, turns=8, repeats=5000)
experiment2 = Experiment(deck=deck2, agent=AI.naive, turns=8, repeats=5000)

results1 = list(experiment1.evaluate([Metric.mean]).values())[0]
results2 = list(experiment2.evaluate([Metric.mean]).values())[0]

for x,y in zip(results1, results2):
    print(x - y)
