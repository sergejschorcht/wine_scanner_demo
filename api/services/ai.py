from typing import Optional, Tuple, List
from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def get_price(self, book_name: str, format_type: Optional[str] = None) -> Tuple[Optional[float], List[str]]:
        pass
