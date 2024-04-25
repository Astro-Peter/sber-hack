from datetime import datetime
import pandas as pd
from abc import ABC, abstractmethod


class SelectFilesAbstract(ABC):
    @abstractmethod
    def get_new_publications(self,
                             from_date: datetime.date,
                             to_date: datetime.date) -> pd.DataFrame:
        pass
