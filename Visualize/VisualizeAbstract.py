from abc import ABC, abstractmethod

import pandas as pd


class VisualizeAbstract(ABC):
    @abstractmethod
    def compare_multiple(self,
                         data: pd.DataFrame,
                         save_as: str):
        pass

    @abstractmethod
    def compare_single(self,
                       data: pd.DataFrame,
                       save_as: str):
        pass