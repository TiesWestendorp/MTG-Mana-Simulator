from models.run_single import run_single

class Experiment:
    def __init__(self, deck, ai, turns, repeats):
        self.deck    = deck
        self.ai      = ai
        self.turns   = turns
        self.repeats = repeats
        self.run()

    def run(self):
        self.traces = [run_single(self.deck, self.ai, self.turns) for _ in range(self.repeats)]
    def evaluate(self, metrics):
        return dict(map(lambda metric: [metric.name, metric.compute(self.traces)], metrics))
