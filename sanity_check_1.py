# Sanity check #1: without ramp or draw, the land per turn distribution corresponds to the hypergeometric distribution


from models import AI, Card, Experiment, Metric
from random import seed

seed(1337)

deck = 38*[Card.untapped_land] + 61*[Card.filler]
experiment = Experiment(deck=deck, ai=AI.naive, turns=8, repeats=15000, options={ 'variance_reduction': 'antithetic-variates' })

results = list(experiment.evaluate([Metric.on_curve]).values())[0]
hypergeometric = [
0.983, # Population: 99, Sample size: 8,  Successes in population: 38, Successes in Sample: 1
0.925, # Population: 99, Sample size: 9,  Successes in population: 38, Successes in Sample: 2
0.819, # Population: 99, Sample size: 10, Successes in population: 38, Successes in Sample: 3
0.676, # Population: 99, Sample size: 11, Successes in population: 38, Successes in Sample: 4
0.519, # Population: 99, Sample size: 12, Successes in population: 38, Successes in Sample: 5
0.372, # Population: 99, Sample size: 13, Successes in population: 38, Successes in Sample: 6
0.250, # Population: 99, Sample size: 14, Successes in population: 38, Successes in Sample: 7
0.158, # Population: 99, Sample size: 15, Successes in population: 38, Successes in Sample: 8
]

for x,y in zip(results, hypergeometric):
    assert abs(x-y)/y < 0.01
