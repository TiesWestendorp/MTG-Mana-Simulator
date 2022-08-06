import matplotlib.pyplot as plt
from mtg_mana_simulator import AI, Card, Experiment, Metric, Sequence

title = "Saffi Eriksdotter"
cmc = 2
number_of_land = 35
deck_size = 99
turns = list(range(1, 11))

avacyns_pilgrim = birds_of_paradise = Card.tapped_rock(1, 1)
sakura_tribe_elder = Card.tapped_rock(2, 1)
burnished_hart = Card(cost=3, mana_sequence=Sequence.repeat(2).prefixed_by([0, -2]))
yavimaya_granger = Card.tapped_rock(3, 1)
yavimaya_elder = Card(cost=3, draw_sequence=Sequence.once(1).prefixed_by([0]), mana_sequence=Sequence.once(-2).prefixed_by([0]))
solemn_simulacrum = Card.tapped_rock(4, 1)
natures_lore = Card.tapped_rock(2, 1)
cultivate = Card.tapped_rock(3, 1)

deck = [
    avacyns_pilgrim,
    birds_of_paradise,
    sakura_tribe_elder,
    burnished_hart,
    yavimaya_elder,
    yavimaya_granger,
    solemn_simulacrum,
    natures_lore,
    cultivate
] + 21*[Card.untapped_land] + 14*[Card.tapped_land]
deck += (99-len(deck))*[Card.filler]

with plt.style.context("bmh"):
    plt.figure(figsize=(8,4), dpi=80)
    experiment = Experiment(deck=deck, ai=AI.less_naive, turns=turns[-1], repeats=10000)
    results = list(experiment.evaluate([
        Metric.on_curve,
        Metric.above_threshold("max_mana", cmc),
        Metric.above_threshold("max_mana", cmc+2),
        Metric.above_threshold("max_mana", cmc+4)
    ]).values())
    plt.plot(turns, results[0], label="Mana≥Turn")
    plt.plot(turns, results[1], label="Mana≥Commander")
    plt.plot(turns, results[2], label="Mana≥Commander+2")
    plt.plot(turns, results[3], label="Mana≥Commander+4")
    plt.legend(loc=1)
    plt.title(title)
    plt.xlabel("Turn")
    plt.ylabel("Probability")
    plt.xticks(turns)
    plt.yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    plt.ylim([0, 1])
    plt.savefig('saffi.png')
