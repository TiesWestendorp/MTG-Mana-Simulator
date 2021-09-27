from models import AI, Card, Experiment, Metric, Sequence

decks = []

# Template 2 (https://mtgdecks.net/Commander/imperio-elfico-decklist-by-rauryson-1157822)
#deck = []
#deck += 5*[Card.tapped_land]
#deck += 25*[Card.untapped_land]
#deck += 7*[Card.tapped_rock(1, 1)] # Fyndhorn Elves/Llanowar Elves/Arbor Elf/Elvish Mystic/Deathrite Shaman/Elves of Deep Shadow/Gnarlroot Trapper
#deck += 1*[Card.tapped_rock(2, 1)] # Incubation Druid
#deck += 1*[Card.tapped_rock(3, 3)] # Elvish Archdruid
#deck += 1*[Card.tapped_rock(3, 1)] # Marwyn, the Nurturer
#deck += 2*[Card.tapped_rock(4, 3)] # Canopy Tactician/Wirewood Channeler
#deck += 1*[Card("Elvish Visionary", False, 2, draw_sequence=Sequence.once(1))]
#deck += (99-len(deck))*[Card.filler]
#decks.append(["cEDH elves", deck])

# Template 3
#deck = []
#deck += 10*[Card.tapped_land]
#deck += 30*[Card.untapped_land]
#deck += [Card.untapped_rock(2, 1)] # Nature's Lore
#deck += 2*[Card.tapped_rock(2, 1)] # Rampant Growth/Sakura-Tribe Elder
#deck += 5*[Card.tapped_rock(3, 1)] # Cultivate/Kodama's Reach/Harrow/Search for Tomorrow/Far Wanderings
#deck += [Card.tapped_rock(4, 2)] # Explosive Vegetation
#deck += [Card.untapped_rock(4, 2)] # Skyshroud Claim
#deck += (99-len(deck))*[Card.filler]
#decks.append(["Lands", deck])

lands = 38*[Card.untapped_land]
ramp_package = []
ramp_package += 4*[Card.untapped_rock(2, 1)] # Signets/Talismans
ramp_package += 4*[Card.untapped_rock(3, 1)] # Lockets/Keyrunes
draw_package = []
draw_package += 3*[Card.cantrip]
draw_package += 2*[Card("Divination", False, 3, draw_sequence=Sequence.once(2))]
draw_package += [Card("Phyrexian Arena", False, 3, draw_sequence=Sequence.one.prefixed_by([0]))]

# Template 4
deck = lands
deck += (99-len(deck))*[Card.filler]
decks.append(["X ramp, X card draw", deck])

deck = lands + draw_package
deck += (99-len(deck))*[Card.filler]
decks.append(["X ramp, ✓ card draw", deck])

deck = lands + ramp_package
deck += (99-len(deck))*[Card.filler]
decks.append(["✓ ramp, X card draw", deck])

deck = lands + ramp_package + draw_package
deck += (99-len(deck))*[Card.filler]
decks.append(["✓ ramp, ✓ card draw", deck])

import numpy as np
import matplotlib.pyplot as plt
x,y = [2,2]
fig, axs = plt.subplots(y,x)
mana_by_turn = []
for i,(ax,(template_name,deck)) in enumerate(zip(axs.flat, decks)):
    experiment = Experiment(deck=deck, ai=AI.less_naive, turns=10, repeats=20000)
    metrics = [Metric.minimum_mana(turn+1) for turn in range(experiment.turns)]
    results = experiment.evaluate(metrics)
    xs = list([turn+1 for turn in range(experiment.turns)])
    print(template_name)
    for name,values in results.items():
        print("  - {}: {}".format(name, values))
        ax.plot(xs, values, label=name)
    print()
    mana_equals_turns = list(experiment.evaluate([Metric.minimum_turn_mana()]).values())[0]
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
