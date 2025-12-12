from abc import ABC, abstractmethod
from dataclasses import dataclass

import torch


@dataclass
class BaseModel(ABC):
    horizont: int = 16

    @abstractmethod
    def predict(self, data: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError
