from typing import Sequence
from pseudorandom import PseudoRandomNumberGenerator


__all__ = ["XORShift"]


class XORShift(PseudoRandomNumberGenerator):
    """XORShift32 algorithm implementation."""

    def __init__(self):
        self._seed = None
        self._generator = None

    def seed(self, seed_value: int):
        self._seed = seed_value
        self._generator = self.random()

    def _xorshift(self):
        self._seed ^= self._seed << 13
        self._seed ^= self._seed >> 17
        self._seed ^= self._seed << 5
        return (self._seed % self.uint32_t) / self.uint32_t

    def random(self):
        if self._seed is None:
            raise ValueError("No seed provided")

        while True:
            yield self._xorshift()

    def uniform(self, low: float = 0.0, high: float = 1.0):
        if self._generator is None:
            raise ValueError("No generator available")

        return low + (high - low) * next(self._generator)

    def randint(self, low: int, high: int):
        if self._generator is None:
            raise ValueError("No generator available")

        return int(low + (high - low + 1) * next(self._generator))

    def choice(self, seq: Sequence):
        if len(seq) == 0:
            raise ValueError("Cannot choose from an empty sequence.")

        index = self.randint(0, len(seq) - 1)
        return seq[index]

    def shuffle(self, seq: Sequence):
        for i in range(len(seq) - 1, 0, -1):
            j = self.randint(0, i)
            seq[i], seq[j] = seq[j], seq[i]
