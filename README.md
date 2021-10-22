# MTG-Mana-Simulator
## Simulate deck plays and track mana metrics

This library models simplified "Magic: the Gathering" playthroughs with the purpose of tracking available mana in each turn. This is modeled as experiments that can be run for a given number of turns and repetitions, where some AI agent decides which cards to play in each turn. The cards themselves are heavily simplified, among others, the following attributes are modeled: the generated mana and gold/treasure when played and on every subsequent turn, the card draw attained when played and on every subsequent turn, the cost of playing it, and whether the card is a land or not. After an experiment has run, metrics can be applied to the generated traces, e.g. to find the probability of being on curve or above in each turn.

### Installation

The latest version of this package on PyPI can be installed through `pip` by executing the following command in your console:
```
pip install mtg-mana-simulator
```
Alternatively, you can install the package as currently found on Github through:
```
pip install git+git://github.com/TiesWestendorp/MTG-Mana-Simulator.git#egg=mtg_mana_simulator
```

### Example
After installing, you can verify whether the package was installed correctly by executing the following example code:

```
from mtg_mana_simulator import AI, Card, Experiment, Metric, Sequence
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

<details>
<summary>Updated example (not published on PyPI yet)</summary>

```
from mtg_mana_simulator import AI, Card, Experiment, Metric, Repository

cards = [
  "Dark Ritual",
  "Phyrexian Arena",
  "Orzhov Locket",
  "Orzhov Signet",
  "Dimir Locket",
  "Dimir Signet",
  "Azorius Guildgate",
  "Dimir Guildgate",
  "Orzhov Guildgate",
  "Crumbling Necropolis",
  "Jwar Isle Refuge",
  "Scoured Barrens",
  "Sejiri Refuge",
  "Tranquil Cove",
  "Illusion of Choice",
  "Peek",
  "Gitaxian Probe",
  *["Swamp"]*10,
  *["Island"]*10,
  *["Plains"]*10,
  *["Filler"]*52
]
deck = list(map(lambda name: Repository[name], cards))

experiment = Experiment(deck=deck, ai=AI.naive, turns=10, repeats=10000)
print(experiment.evaluate([Metric.on_curve]))
```
Which ought to print: `{"≥'turn' mana": [0.9588, 0.9016, 0.8313, 0.7492, 0.637, 0.5235, 0.4113, 0.314, 0.229, 0.1653]}`. Which can be interpreted as there being a 75% chance to be on or ahead of curve in turn 4 for this given deck (of course, due to random variations, this number may be slightly different for you).
</details>

### Output of examples/main.py
![Comparison of mana per turn probabilities of decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_1.png?raw=true)
![Probability of being on curve for decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_2.png?raw=true)
![Average mana per turn for decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_3.png?raw=true)
![Percentiles of available mana for decks with/without ramp/card draw](https://github.com/TiesWestendorp/MTG-Mana-Simulator/blob/master/Figure_4.png?raw=true)

Ramp package: 3 elves, 4 talismans, 4 lockets, 1 Smothering Tithe

Draw package: 3 cantrips, 1 Divination, 1 Phyrexian Arena
