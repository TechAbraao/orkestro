from abc import ABC, abstractmethod
from typing import Any, List, Optional

class CRUDInterface(ABC):
    @abstractmethod
    def get(self, entity_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def all(self) -> List[Any]:
        pass

    @abstractmethod
    def create(self, data: dict) -> Any:
        pass

    @abstractmethod
    def update(self, entity_id: int, data: dict) -> bool:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        pass
