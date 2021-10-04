"""
Defines the Sequence class which provides a way to create generators of integers that
iterate a finite list followed by a repeating pattern, as well as logic to compose
them.
"""

from typing import List, Iterator
from math import ceil
from models.helpers import divisors, lcm

class Sequence:
    """Infinite sequence of integers consisting of a finite prefix and a repeating pattern"""

    zero : "Sequence"
    one  : "Sequence"

    def __init__(self, prefix: List[int], pattern: List[int]) -> None:
        self.prefix = prefix
        self.pattern = pattern if len(pattern) > 0 else [0]
        self.normalize()

    def normalize(self) -> "Sequence":
        """Normalizes the sequence, such that comparison can be done elementwise"""
        # Reduce prefix size by 'rotating' the repeated pattern
        while len(self.prefix) > 0 and self.prefix[-1] == self.pattern[-1]:
            self.prefix = self.prefix[:-1]
            self.pattern = self.pattern[-1:]+self.pattern[:-1]

        # Reduce pattern size by identifying sublist that multiply
        for divisor in divisors(len(self.pattern)):
            times = len(self.pattern)//divisor
            if self.pattern == times*self.pattern[:divisor]:
                self.pattern = self.pattern[:divisor]
                break
        return self

    # Assumes the sequences are normalized
    def __eq__(self, other) -> bool:
        if not isinstance(other, Sequence):
            return NotImplemented
        return self.prefix == other.prefix and self.pattern == other.pattern

    def __add__(self, other: 'Sequence') -> 'Sequence':
        prefix_length = max([len(self.prefix), len(other.prefix)])
        pattern_length = lcm(len(self.pattern), len(other.pattern))
        prefix1 = self.finite_prefix(prefix_length + pattern_length)
        prefix2 = other.finite_prefix(prefix_length + pattern_length)
        summed: List[int] = list(map(sum, zip(prefix1, prefix2)))
        return Sequence(summed[:prefix_length], summed[prefix_length:]).normalize()

    def prefixed_by(self, additional_prefix: List[int]) -> 'Sequence':
        """Prefix an additional number to the sequence"""
        return Sequence(additional_prefix + self.prefix, self.pattern).normalize()

    def finite_prefix(self, length: int) -> List[int]:
        """Returns finite prefix of the sequence of the given length"""
        if length <= len(self.prefix):
            return self.prefix[:length]
        times = ceil((length - len(self.prefix))/len(self.pattern))
        return (self.prefix + times*self.pattern)[:length]

    def generator(self) -> Iterator[int]:
        """Returns a generator that iterates the sequence"""
        for element in self.prefix:
            yield element
        while True:
            for element in self.pattern:
                yield element

    @staticmethod
    def once(number: int) -> 'Sequence':
        """Returns a sequence of all zeroes prefixed by the given number"""
        return Sequence([number], []).normalize()

    @staticmethod
    def repeat(number: int) -> 'Sequence':
        """Returns a sequence infinitely repeating the given number"""
        return Sequence([], [number])

Sequence.zero = Sequence.repeat(0) # The all zeroes sequence: 0, 0, 0, ...
Sequence.one  = Sequence.repeat(1) # The all ones sequence:   1, 1, 1, ...
