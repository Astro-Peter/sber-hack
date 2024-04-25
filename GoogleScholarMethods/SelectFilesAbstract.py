from datetime import datetime
import pandas as pd


class SelectFilesAbstract:
    def getNewPublications(self,
                           from_date: datetime.date,
                           to_date: datetime.date) -> pd.DataFrame:
        pass
