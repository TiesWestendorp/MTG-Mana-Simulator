# MTG-Mana-Simulator
## Simulate deck plays and track mana metrics

This library models simplified "Magic: the Gathering" playthroughs with the purpose of tracking available mana in each turn. This is modeled as experiments that can be run for a given number of turns and repetitions, where some AI agent decides which cards to play in each turn. The cards themselves are heavily simplified, among others, the following attributes are modeled: the generated mana and gold/treasure when played and on every subsequent turn, the card draw attained when played and on every subsequent turn, the cost of playing it, and whether the card is a land or not. After an experiment has run, metrics can be applied to the generated traces, e.g. to find the probability of being on curve or above in each turn.

### Example
```
from models import AI, Card, Experiment, Metric, Sequence

dark_ritual     = Card(cost=1, mana_sequence=Sequence.once(3))
phyrexian_arena = Card(cost=3, draw_sequence=Sequence.one.prefixed_by([0]))
signet          = Card.untapped_rock(2, 1)
locket          = Card.untapped_rock(3, 1)

deck = [
  dark_ritual,
  phyrexian_arena,
  *[signet, locket]*2,
  *[Card.cantrip]*3,
  *[Card.untapped_land]*30,
  *[Card.tapped_land]*8,
  *[Card.filler]*54
]

experiment = Experiment(deck=deck, ai=AI.naive, turns=10, repeats=10000)
experiment.evaluate([Metric.on_curve])

# {"≥'turn' mana": [0.9554, 0.8848, 0.8128, 0.7195, 0.6196, 0.5061, 0.3904, 0.2906, 0.2199, 0.1601]}
# E.g. there's a 72% chance to be on or ahead of curve in turn 4
```

### Output of examples/main.py
![Comparison of mana per turn probabilities of decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_1.png?raw=true)
![Probability of being on curve for decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_2.png?raw=true)
![Average mana per turn for decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_3.png?raw=true)

Ramp package: 3 elves, 4 talismans, 4 lockets, 1 Smothering Tithe

Draw package: 3 cantrips, 1 Divination, 1 Phyrexian Arena
