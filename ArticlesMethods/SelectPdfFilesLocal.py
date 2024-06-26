import pandas as pd

from datetime import date
from ArticlesMethods.SelectFilesAbstract import SelectFilesAbstract


class SelectPdfFilesLocal(SelectFilesAbstract):
    def get_new_publications(self,
                             from_date: date,
                             to_date: date) -> pd.DataFrame:
        data = pd.read_csv("stats.csv")
        return data[(data["date"] <= to_date.strftime("%Y-%m-%d")) & (data["date"] >= from_date.strftime("%Y-%m-%d"))]
