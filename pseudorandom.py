from abc import ABC, abstractmethod
from typing import Generator, Sequence


class PseudoRandomNumberGenerator(ABC):
    """Abstract base class for Pseudo Random Number Generators."""

    # 32-bit integer size
    uint32_t: int = 2**32

    @abstractmethod
    def seed(self, seed_value: int):
        """
        Seed the random number generator with a given value
        and initialize the generator
        """
        pass

    @abstractmethod
    def random(self) -> Generator[int, None, None]:
        """
        Return the generator object.

        :throws: ValueError if no seed is provided
        """
        pass

    @abstractmethod
    def uniform(self, low: float = 0.0, high: float = 1.0) -> float:
        """
        Return a random floating point number in the range [low, high)
        or [0.0, 1.0) if no range is specified.

        :throws: ValueError if no generator is specified
        """
        pass

    @abstractmethod
    def randint(self, low: int, high: int) -> int:
        """
        Return a random integer in the range [low, high].

        :throws: ValueError if no generator is specified
        """
        pass

    @abstractmethod
    def choice(self, seq: Sequence) -> any:
        """
        Return a random element from the non-empty sequence.

        :throws: ValueError if sequence is empty
        """
        pass

    @abstractmethod
    def shuffle(self, seq: Sequence) -> None:
        """
        Shuffle the sequence in place.
        """
        pass
