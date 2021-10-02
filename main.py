"""
Plots several metrics of templates.
"""

import matplotlib.pyplot as plt
from models import AI, Card, Experiment, Metric, Sequence

AI = AI.naive
TURNS = 10
REPEATS = 10000
OPTIONS = { 'variance_reduction': 'antithetic-variates' }

dark_ritual        = Card("Dark Ritual", cost=1, mana_sequence=Sequence.once(3))
elf                = Card.tapped_rock(1, 1)
sign_in_blood      = Card.draw_spell(2, 2)
talisman           = Card.untapped_rock(2, 1)
divination         = Card.draw_spell(3, 2)
locket             = Card.untapped_rock(3, 1)
phyrexian_arena    = Card("Phyrexian Arena", cost=3, draw_sequence=Sequence.one.prefixed_by([0]))
smothering_tithe   = Card("Smothering Tithe", cost=4, gold_sequence=Sequence.repeat(3).prefixed_by([0]))
bounty_of_the_luxa = Card("Bounty of the Luxa", cost=4, mana_sequence=Sequence([0], [0, 3]), draw_sequence=Sequence([], [0, 1]))

lands        = 38*[Card.untapped_land]
ramp_package = 4*[elf] + 4*[talisman] + 4*[locket] + [smothering_tithe]
draw_package = 6*[Card.cantrip] + [sign_in_blood, divination, phyrexian_arena]

decks = []
decks.append(["x ramp, x card draw", lands[:]])
decks.append(["x ramp, ✓ card draw", lands[:] + draw_package[:]])
decks.append(["✓ ramp, x card draw", lands[:] + ramp_package[:]])
decks.append(["✓ ramp, ✓ card draw", lands[:] + ramp_package[:] + draw_package[:]])

for _,deck in decks:
    deck += (99-len(deck))*[Card.filler]

x,y = [2,2]
xs = [turn+1 for turn in range(TURNS)]

experiments = [Experiment(deck=deck, ai=AI, turns=TURNS, repeats=REPEATS, options=OPTIONS) for _,deck in decks]
metrics = [Metric.minimum_mana(turn+1) for turn in range(TURNS)] + [Metric.on_curve, Metric.above_curve]
percentiles = [Metric.mean, Metric.percentile(0.001), Metric.percentile(0.25), Metric.percentile(0.5), Metric.percentile(0.75), Metric.percentile(1.0)]

fig, axs = plt.subplots(y,x)
for i,(ax,(name,_),experiment) in enumerate(zip(axs.flat, decks, experiments)):
    for j,(metric,values) in enumerate(experiment.evaluate(metrics).items()):
        if j<len(metrics)-1:
            ax.plot(xs, values, label=metric)
        else:
            ax.plot(xs, values, 'g--', label=metric)
    if i%2 == 0:
        ax.set(ylabel='Probability')
    if i>=x*(y-1):
        ax.set(xlabel='Turns')
    ax.set_title(name)
    ax.set_xticks([turn+1 for turn in range(TURNS)])
    ax.legend(loc=2, prop={'size': 4})
plt.tight_layout()
plt.show()

for (name,deck),values in zip(decks, [list(experiment.evaluate([Metric.on_curve]).values())[0] for experiment in experiments]):
    plt.plot(xs, values, label=name)
plt.legend(loc=3, prop={'size': 6})
plt.show()

for (name,deck),values in zip(decks, [list(experiment.evaluate([Metric.mean]).values())[0] for experiment in experiments]):
    plt.plot(xs, values, label=name)
plt.legend(loc=2, prop={'size': 6})
plt.show()

fig, axs = plt.subplots(y,x)
for i,(ax,(name, _),experiment) in enumerate(zip(axs.flat, decks, experiments)):
    for metric,values in experiment.evaluate(percentiles).items():
        ax.plot(xs, values, label=metric)
    if i%2 == 0:
        ax.set(ylabel='Mana')
    if i>=x*(y-1):
        ax.set(xlabel='Turns')
    ax.set_title(name)
    ax.set_xticks([turn+1 for turn in range(TURNS)])
    ax.legend(loc=2, prop={'size': 4})
plt.tight_layout()
plt.show()
