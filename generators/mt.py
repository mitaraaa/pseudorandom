import random
from typing import Generator, Sequence

from pseudorandom import PseudoRandomNumberGenerator


__all__ = ["MersenneTwister"]


class MersenneTwister(PseudoRandomNumberGenerator):
    def __init__(self):
        self._seed = None
        self._generator = None

    def seed(self, seed_value: int):
        self._seed = seed_value

        random.seed(self._seed)
        self._generator = self.random()

    def random(self) -> Generator[int, None, None]:
        if self._seed is None:
            raise ValueError("No seed is provided")

        while True:
            yield random.randint(0, 2**32 - 1)

    def uniform(self, low: float = 0.0, high: float = 1.0) -> float:
        if self._generator is None:
            raise ValueError("No generator is specified")

        return random.uniform(low, high)

    def randint(self, low: int, high: int) -> int:
        if self._generator is None:
            raise ValueError("No generator is specified")

        return random.randint(low, high)

    def choice(self, seq: Sequence) -> any:
        if not seq:
            raise ValueError("Sequence is empty")

        if self._generator is None:
            raise ValueError("No generator is specified")

        return random.choice(seq)

    def shuffle(self, seq: Sequence) -> None:
        if self._generator is None:
            raise ValueError("No generator is specified")

        random.shuffle(seq)
