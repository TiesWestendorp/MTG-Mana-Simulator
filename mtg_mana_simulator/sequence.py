"""
Defines the Sequence class which provides a way to create generators of integers that
iterate a finite list followed by a repeating pattern, as well as logic to compose
them.
"""

from typing import Callable, List, Iterator, Tuple
from math import ceil
from mtg_mana_simulator.helpers import divisors, lcm

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

    def __getitem__(self, key: int) -> int:
        if key < len(self.prefix):
            return self.prefix[key]
        return self.pattern[(key - len(self.prefix)) % len(self.pattern)]

    def __add__(self, other: 'Sequence') -> 'Sequence':
        return self.compose(sum, other)

    def __sub__(self, other: 'Sequence') -> 'Sequence':
        return self.compose(lambda x: x[0]-x[1], other)

    def improvement_over(self, other: 'Sequence') -> 'Sequence':
        """Returns the improvement this sequence gives over the current one"""
        return self.compose(max, other) - other

    def compose(self, func: Callable[[Tuple[int, int]], int], other: 'Sequence') -> 'Sequence':
        """Perform elementwise operation on two sequences to create a new one"""
        prefix_length = max(len(self.prefix), len(other.prefix))
        pattern_length = lcm(len(self.pattern), len(other.pattern))
        prefix1 = self.finite_prefix(prefix_length + pattern_length)
        prefix2 = other.finite_prefix(prefix_length + pattern_length)
        composed: List[int] = list(map(func, zip(prefix1, prefix2)))
        return Sequence(composed[:prefix_length], composed[prefix_length:]).normalize()

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

    def take(self, number: int) -> 'Sequence':
        """Returns a new sequence, where the first number of elements have been removed"""
        if number <= len(self.prefix):
            return Sequence(self.prefix[number:], self.pattern)
        number = (number - len(self.prefix)) % len(self.pattern)
        return Sequence([], self.pattern[number:] + self.pattern[:number])

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
