import matplotlib.pyplot as plt
from mtg_mana_simulator import AI, Card, Experiment, Metric, Sequence

number_of_land = 38
deck_size = 99
turns = list(range(4, 11))

bounty_of_the_luxa = Card(cost=4, draw_sequence=Sequence([], [0, 1]), mana_sequence=Sequence([0], [0, 1]))
phyrexian_arena    = Card(cost=3, draw_sequence=Sequence.one.prefixed_by([0]))
smothering_tithe   = Card(cost=4, gold_sequence=Sequence.one.prefixed_by([0]))

land_package = 38*[Card.untapped_land]

decks = []
decks.append(["38 lands", land_package[:]])
decks.append(["+ Bounty of the Luxa", land_package[:] + [bounty_of_the_luxa]])
decks.append(["+ Phyrexian Arena", land_package[:] + [phyrexian_arena]])
decks.append(["+ Smothering Tithe", land_package[:] + [smothering_tithe]])
for _,deck in decks:
    deck += (99-len(deck))*[Card.filler]

with plt.style.context("bmh"):
    plt.figure(figsize=(8,4), dpi=80)
    for title,deck in decks:
        experiment = Experiment(deck=deck, ai=AI.naive, turns=turns[-1], repeats=10000)
        results = list(experiment.evaluate([Metric.on_curve]).values())[0][turns[0]-1:]
        plt.plot(turns, results, label=title)
    plt.legend(loc=1)
    plt.title("Probability of being on curve")
    plt.xlabel("Turn")
    plt.ylabel("P( mana ≥ turn )")
    plt.xticks(turns)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8])
    plt.savefig('plot2.png')
