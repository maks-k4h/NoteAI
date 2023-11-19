import numpy as np
from abc import ABC, abstractmethod


class EmbeddingStrategy(ABC):

    @abstractmethod
    def encode(self, text: str | list[str]) -> np.ndarray:
        pass


