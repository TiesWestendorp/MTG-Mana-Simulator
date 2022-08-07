import matplotlib.pyplot as plt
from mtg_mana_simulator import AI, Card, Experiment, Metric, Sequence
from mtg_mana_simulator.actions import basic_tapped_into_play, basic_untapped_into_play, basic_to_hand
from mtg_mana_simulator.repository import Repository

title = "Saffi Eriksdotter"
cmc = 2
number_of_land = 35
deck_size = 99
turns = list(range(1, 11))

avacyns_pilgrim = birds_of_paradise = Card.tapped_rock(1, 1)
sakura_tribe_elder = Card("Sakura-Tribe Elder", cost=2, transform=[basic_tapped_into_play])
burnished_hart = Card(cost=3, mana_sequence=Sequence.repeat(2).prefixed_by([0, -2]))
yavimaya_granger = Card("Yavimaya Granger", cost=3, transform=[basic_tapped_into_play])
yavimaya_elder = Card(cost=3, draw_sequence=Sequence.once(1).prefixed_by([0]), mana_sequence=Sequence.once(-2).prefixed_by([0]))
solemn_simulacrum = Card("Solemn Simulacrum", cost=4, transform=[basic_tapped_into_play])

deck = [
    avacyns_pilgrim,
    birds_of_paradise,
    sakura_tribe_elder,
    burnished_hart,
    yavimaya_elder,
    yavimaya_granger,
    solemn_simulacrum,
    Repository["Nature's Lore"],
    Repository['Cultivate']
] + 21*[Card.basic_land] + 5*[Card.untapped_land] + 9*[Card.tapped_land]
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
