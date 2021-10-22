import matplotlib.pyplot as plt
from scipy.stats import binom, hypergeom

proportion_land = 1/3
deck_size = 99

turns = list(range(1, 11))
binomial       = [1 - binom.cdf(turn-1, 6+turn, proportion_land) for turn in turns]
hypergeometric = [1 - hypergeom.cdf(turn-1, deck_size, 6+turn, round(deck_size*proportion_land)) for turn in turns]

with plt.style.context("bmh"):
    plt.figure(figsize=(8,4), dpi=80)
    plt.plot(turns, binomial, label="Binomial")
    plt.plot(turns, hypergeometric, label="Hypergeometric")
    plt.legend(loc=1)
    plt.title("Probability of being on curve")
    plt.xlabel("Turn")
    plt.ylabel("P( mana ≥ turn )")
    plt.xticks(turns)
    plt.yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    plt.savefig('plot1.png')
