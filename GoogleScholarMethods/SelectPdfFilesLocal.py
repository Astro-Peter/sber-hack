import pandas as pd

from datetime import date
from GoogleScholarMethods.SelectFilesAbstract import SelectFilesAbstract


class SelectPdfFilesLocal(SelectFilesAbstract):
    def getNewPublications(self,
                           from_date: date,
                           to_date: date) -> pd.DataFrame:
        data = pd.read_csv("stats.csv")
        return data[(data["date"] <= to_date) & (data["date"] >= from_date)]
