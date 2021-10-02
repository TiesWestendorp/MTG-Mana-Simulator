from typing import List, Iterator
from math import ceil
from models.helpers import divisors, lcm

class Sequence:
    """Infinite sequence of integers consisting of a finite prefix and a repeating part"""

    zero = None
    one  = None

    def __init__(self, prefix: List[int], repeat: List[int]) -> None:
        self.prefix = prefix
        self.repeat = repeat if len(repeat) > 0 else [0]
        self.normalize()

    def normalize(self):
        """Normalizes the sequence, such that comparison can be done elementwise"""
        # Reduce prefix size by 'rotating' the repeated part
        while len(self.prefix) > 0 and self.prefix[-1] == self.repeat[-1]:
            self.prefix = self.prefix[:-1]
            self.repeat = self.repeat[-1:]+self.repeat[:-1]

        # Reduce repeated size by identifying sublist that multiply
        for divisor in divisors(len(self.repeat)):
            times = len(self.repeat)//divisor
            if self.repeat == times*self.repeat[:divisor]:
                self.repeat = self.repeat[:divisor]
                break
        return self

    # Assumes the sequences are normalized
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
        """Prefix an additional number to the sequence"""
        return Sequence(additional_prefix + self.prefix, self.repeat)

    def finite_prefix(self, length: int) -> List[int]:
        """Returns finite prefix of the sequence of the given length"""
        k = ceil((length - len(self.prefix))/len(self.repeat))
        return (self.prefix + k*self.repeat)[:length]

    def generator(self) -> Iterator[int]:
        """Returns a generator that iterates the sequence"""
        for element in self.prefix:
            yield element
        while True:
            for element in self.repeat:
                yield element

    @staticmethod
    def once(number: int) -> 'Sequence':
        """Returns a sequence of all zeroes prefixed by the given number"""
        return Sequence([number], [])

    @staticmethod
    def repeat(number: int) -> 'Sequence':
        """Returns a sequence infinitely repeating the given number"""
        return Sequence([], [number])

Sequence.zero = Sequence.repeat(0) # The all zeroes sequence: 0, 0, 0, ...
Sequence.one  = Sequence.repeat(1) # The all ones sequence:   1, 1, 1, ...
