import matplotlib.pyplot as plt
from mtg_mana_simulator import AI, Card, Experiment, Metric, Sequence

number_of_land = 38
deck_size = 99
turns = list(range(1, 11))

elf              = Card.tapped_rock(1, 1)
sign_in_blood    = Card.draw_spell(2, 2)
talisman         = Card.untapped_rock(2, 1)
divination       = Card.draw_spell(3, 2)
locket           = Card.untapped_rock(3, 1)
phyrexian_arena  = Card(cost=3, draw_sequence=Sequence.one.prefixed_by([0]))
smothering_tithe = Card(cost=4, gold_sequence=Sequence.repeat(3).prefixed_by([0]))

land_package = 38*[Card.untapped_land]
ramp_package = 4*[elf] + 4*[talisman] + 4*[locket] + [smothering_tithe]
draw_package = 6*[Card.cantrip] + [sign_in_blood, divination, phyrexian_arena]

decks = []
decks.append(["x ramp, x card draw", land_package[:]])
decks.append(["x ramp, ✓ card draw", land_package[:] + draw_package[:]])
decks.append(["✓ ramp, x card draw", land_package[:] + ramp_package[:]])
decks.append(["✓ ramp, ✓ card draw", land_package[:] + ramp_package[:] + draw_package[:]])
for _,deck in decks:
    deck += (99-len(deck))*[Card.filler]

with plt.style.context("bmh"):
    plt.figure(figsize=(8,4), dpi=80)
    for title,deck in decks:
        experiment = Experiment(deck=deck, ai=AI.naive, turns=turns[-1], repeats=10000)
        results = list(experiment.evaluate([Metric.on_curve]).values())[0]
        plt.plot(turns, results, label=title)
    plt.legend(loc=1)
    plt.title("Probability of being on curve")
    plt.xlabel("Turn")
    plt.ylabel("P( mana ≥ turn )")
    plt.xticks(turns)
    plt.yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    plt.savefig('plot3.png')
