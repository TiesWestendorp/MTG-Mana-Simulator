from typing import List, Iterator
from math import ceil

class Sequence:
    zero = None
    one  = None

    def __init__(self: 'Sequence', prefix: List[int], repeat: List[int]):
        self.prefix = prefix
        self.repeat = repeat if len(repeat) > 0 else [0]
        self.normalize()

    def normalize(self):
        while len(self.prefix) > 0 and self.prefix[-1] == self.repeat[-1]:
            self.prefix = self.prefix[:-1]
            self.repeat = self.repeat[-1:]+self.repeat[:-1]

    def __eq__(self: 'Sequence', other: 'Sequence') -> bool:
        return self.prefix == other.prefix and self.repeat == other.repeat

    def prefixed_by(self, additional_prefix: List[int]) -> 'Sequence':
        return Sequence(additional_prefix + self.prefix, self.repeat)

    # Returns finite prefixes of length n of the sequence
    def finite_prefix(self: 'Sequence', n: int) -> List[int]:
        k = ceil((n - len(self.prefix))/len(self.repeat))
        return (self.prefix + k*self.repeat)[:n]

    # Returns a generator that iterates the sequence
    def generator(self: 'Sequence') -> Iterator[int]:
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
