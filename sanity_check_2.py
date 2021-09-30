from models import AI, Card, Experiment, Metric

deck = 93*[Card.untapped_land] + 6*[Card.filler]
experiment = Experiment(deck=deck, ai=AI.naive, turns=8, repeats=1)

results = list(experiment.evaluate([Metric.minimum_turn_mana]).values())[0]

for x in results:
    assert x == 1.0
