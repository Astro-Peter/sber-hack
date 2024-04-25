from abc import ABC, abstractmethod


class GigaChainMethodsAbstract(ABC):
    # Get themes of the publication using gigachat, returns a dictionary where keys are the themes and values
    # are the evaluation made by the LLM about how prevalent that theme is
    @abstractmethod
    def get_themes(self,
                   text: str) -> dict:
        pass
