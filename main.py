from models import AI, Card, Experiment, Metric
metrics = [Metric.mode, Metric.minimum_mana(4)]

# Sample: https://deckbox.org/sets/2540646
deck = 10*[Card.tapped_land] + 25*[Card.untapped_land] + 6*[Card.untapped_rock(2, 1)] + 2*[Card.untapped_rock(3, 1)] + 56*[Card.filler]
experiment = Experiment(deck=deck, ai=AI.naive, turns=10, repeats=20000)
print("Kykar:", experiment.evaluate(metrics))

# Sample: https://deckbox.org/sets/1890455
deck = 1*[Card.tapped_land] + 34*[Card.untapped_land] + [Card.untapped_rock(4, 3)] + 2*[Card.untapped_rock(2, 1)] + 61*[Card.filler]
experiment = Experiment(deck=deck, ai=AI.naive, turns=10, repeats=20000)
print("Braids:", experiment.evaluate(metrics))
