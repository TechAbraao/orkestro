from abc import ABC, abstractmethod
from typing import Any, Dict


class EntityContract(ABC):
    @property
    @abstractmethod
    def id(self) -> Any:
        pass

    @property
    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        pass
