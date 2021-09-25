class Metric:
    mean = None
    median = None
    mode = None

    def __init__(self, name, func):
        self.name = name
        self.func = func
    def compute(self, traces):
        return [self.func(turn+1, manas_by_turn) for turn,manas_by_turn in enumerate(zip(*traces))]

    @staticmethod
    def minimum_mana(min_mana):
        return Metric("Probability of at least {} mana".format(min_mana), lambda turn,manas_by_turn: sum(mana >= min_mana for mana in manas_by_turn)/len(manas_by_turn))

from statistics import mean, median, mode
Metric.mean   = Metric("Mean",   lambda turn,manas_by_turn: mean(manas_by_turn))
Metric.median = Metric("Median", lambda turn,manas_by_turn: median(manas_by_turn))
Metric.mode   = Metric("Mode",   lambda turn,manas_by_turn: mode(manas_by_turn))
