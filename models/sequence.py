from typing import List, Iterator
from math import ceil

from models.helpers import divisors, lcm

class Sequence:
    zero = None
    one  = None

    def __init__(self, prefix: List[int], repeat: List[int]) -> None:
        self.prefix = prefix
        self.repeat = repeat if len(repeat) > 0 else [0]
        self.normalize()

    def normalize(self):
        # Reduce prefix size by 'rotating' the repeated part
        while len(self.prefix) > 0 and self.prefix[-1] == self.repeat[-1]:
            self.prefix = self.prefix[:-1]
            self.repeat = self.repeat[-1:]+self.repeat[:-1]

        # Reduce repeated size by identifying sublist that multiply
        for d in divisors(len(self.repeat)):
            times = len(self.repeat)//d
            if self.repeat == times*self.repeat[:d]:
                self.repeat = self.repeat[:d]
                break
        return self

    def __eq__(self, other: 'Sequence') -> bool:
        return self.prefix == other.prefix and self.repeat == other.repeat

    def __add__(self, other: 'Sequence') -> 'Sequence':
        prefix_length = max([len(self.prefix), len(other.prefix)])
        repeat_length = lcm(len(self.repeat), len(other.repeat))
        prefix1 = self.finite_prefix(prefix_length + repeat_length)
        prefix2 = other.finite_prefix(prefix_length + repeat_length)
        summed = list(map(sum, zip(prefix1, prefix2)))
        return Sequence(summed[:prefix_length], summed[prefix_length:]).normalize()

    def prefixed_by(self, additional_prefix: List[int]) -> 'Sequence':
        return Sequence(additional_prefix + self.prefix, self.repeat)

    # Returns finite prefixes of length n of the sequence
    def finite_prefix(self, n: int) -> List[int]:
        k = ceil((n - len(self.prefix))/len(self.repeat))
        return (self.prefix + k*self.repeat)[:n]

    # Returns a generator that iterates the sequence
    def generator(self) -> Iterator[int]:
        for element in self.prefix:
            yield element
        while True:
            for element in self.repeat:
                yield element

    @staticmethod
    def once(n: int) -> 'Sequence':
        return Sequence([n], [])
    @staticmethod
    def repeat(n: int) -> 'Sequence':
        return Sequence([], [n])

Sequence.zero = Sequence.repeat(0) # The all zeroes sequence: 0, 0, 0, ...
Sequence.one  = Sequence.repeat(1) # The all ones sequence:   1, 1, 1, ...
