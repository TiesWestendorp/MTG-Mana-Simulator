import matplotlib.pyplot as plt
from mtg_mana_simulator import AI, Card, Experiment, Metric, Sequence, Repository

deck_size = 99
turns = list(range(1, 11))

gitaxian_probe   = Card.draw_spell(0, 1)
arcums_astrolabe = Card.cantrip
sign_in_blood    = Card.draw_spell(2, 2)
divination       = Card.draw_spell(3, 2)
syphon_mind      = Card.draw_spell(4, 3)
phyrexian_arena  = Card(cost=3, draw_sequence=Sequence.one.prefixed_by([0]))

land_package = 38*[Card.basic_land]
rock_package = 10*[Card.tapped_rock(2, 1)]
fetch_package = 10*[Repository["Nature's Lore"]]
draw_package = [
    gitaxian_probe,
    arcums_astrolabe,
    sign_in_blood,
    divination,
    syphon_mind,
    phyrexian_arena
]

decks = []
decks.append(["Rocks", land_package[:] + rock_package[:]])
decks.append(["Land search", land_package[:] + fetch_package[:]])
decks.append(["Rocks + Draw", land_package[:] + rock_package[:] + draw_package[:]])
decks.append(["Land search + Draw", land_package[:] + fetch_package[:] + draw_package[:]])
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
    plt.ylim([0, 1])
    plt.savefig('plot5.png')
