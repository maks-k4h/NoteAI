import numpy as np
from .abs_strategy import EmbeddingStrategy


class EmbeddingContext:
    _strategy: EmbeddingStrategy

    def __int__(self, strategy: EmbeddingStrategy):
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: EmbeddingStrategy):
        self._strategy = strategy

    def encode(self, text: str | list[str]) -> np.ndarray:
        pass



