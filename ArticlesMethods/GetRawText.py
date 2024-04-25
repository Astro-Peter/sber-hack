from abc import ABC, abstractmethod


class GetRawText(ABC):
    @abstractmethod
    def get_text(self,
                 file: str) -> str:
        pass
