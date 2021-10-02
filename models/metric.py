class Metric:
    mean = None
    median = None
    mode = None
    below_curve = None
    on_curve = None
    above_curve = None

    def __init__(self, name, func):
        self.name = name
        self.func = func
    def compute(self, traces):
        return [self.func(turn+1, manas_by_turn) for turn,manas_by_turn in enumerate(zip(*traces))]

    @staticmethod
    def minimum_mana(min_mana: int):
        return Metric("≥{} mana".format(min_mana), lambda turn,manas_by_turn: sum(mana >= min_mana for mana in manas_by_turn)/len(manas_by_turn))
    @staticmethod
    def percentile(p: float):
        return Metric("{}th percentile".format(p), lambda turn,manas_by_turn: sorted(manas_by_turn)[round(len(manas_by_turn)*p)-1])

from statistics import mean, median, mode, variance
Metric.mean   = Metric("Mean",   lambda turn,manas_by_turn:     mean(manas_by_turn))
Metric.median = Metric("Median", lambda turn,manas_by_turn:     int(median(manas_by_turn)))
Metric.mode   = Metric("Mode",   lambda turn,manas_by_turn:     mode(manas_by_turn))
Metric.variance = Metric("Variance", lambda turn,manas_by_turn: variance(manas_by_turn))

Metric.below_curve = Metric("<'turn' mana", lambda turn,manas_by_turn: sum(mana < turn  for mana in manas_by_turn)/len(manas_by_turn))
Metric.on_curve    = Metric("≥'turn' mana", lambda turn,manas_by_turn: sum(mana >= turn for mana in manas_by_turn)/len(manas_by_turn))
Metric.above_curve = Metric(">'turn' mana", lambda turn,manas_by_turn: sum(mana > turn  for mana in manas_by_turn)/len(manas_by_turn))
