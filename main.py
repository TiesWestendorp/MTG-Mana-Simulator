from models import AI, Card, Experiment, Metric, Sequence

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
ramp_package = 3*[elf] + 4*[talisman] + 4*[locket] + [smothering_tithe]
draw_package = 4*[Card.cantrip] + [sign_in_blood, divination, phyrexian_arena]

decks = []
decks.append(["x ramp, x card draw", lands[:]])
decks.append(["x ramp, ✓ card draw", lands[:] + draw_package[:]])
decks.append(["✓ ramp, x card draw", lands[:] + ramp_package[:]])
decks.append(["✓ ramp, ✓ card draw", lands[:] + ramp_package[:] + draw_package[:]])

for _,deck in decks:
    deck += (99-len(deck))*[Card.filler]

import numpy as np
import matplotlib.pyplot as plt
x,y = [2,2]
fig, axs = plt.subplots(y,x)
mana_by_turn = []
for i,(ax,(template_name,deck)) in enumerate(zip(axs.flat, decks)):
    experiment = Experiment(deck=deck, ai=AI.less_naive, turns=10, repeats=30000, options={ 'variance_reduction': 'antithetic-variates' })
    metrics = [Metric.minimum_mana(turn+1) for turn in range(experiment.turns)]
    results = experiment.evaluate(metrics)
    xs = list([turn+1 for turn in range(experiment.turns)])
    print(template_name)
    for name,values in results.items():
        print("  - {}: {}".format(name, values))
        ax.plot(xs, values, label=name)
    print()
    mana_equals_turns = list(experiment.evaluate([Metric.minimum_turn_mana]).values())[0]
    mana_by_turn.append(mana_equals_turns)
    ax.plot(xs, mana_equals_turns, 'g--', label="≥'turn' mana")
    ax.set_xticks([turn+1 for turn in range(experiment.turns)])
    if i%2 == 0:
        ax.set(ylabel='Probability')
    if i>=x*(y-1):
        ax.set(xlabel='Turns')
    ax.set_title(template_name)
axs.flat[-1].legend(loc=1, prop={'size': 4})
plt.tight_layout()
plt.show()

for (template_name, _), res in zip(decks, mana_by_turn):
    plt.plot(xs, res, label=template_name)
plt.xlabel('Turns')
plt.ylabel('Probability')
plt.xticks([turn+1 for turn in range(experiment.turns)])
plt.ylim([0, 1])
plt.legend(loc=1, prop={'size': 6})
plt.show()
