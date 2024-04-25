import pandas as pd

from datetime import date
from GoogleScholarMethods.SelectFilesAbstract import SelectFilesAbstract


class SelectPdfFilesLocal(SelectFilesAbstract):
    def getNewPublications(self,
                           from_date: date,
                           to_date: date) -> pd.DataFrame:
        data = {"date": [], "cities": [], "url": []}

        with open("stats.csv", "rb") as csv:
            for line in csv.readlines():
                words = line.__str__().split(";")
                submitted_date = date.fromisoformat(words[0][2:])
                if submitted_date < from_date or submitted_date > to_date:
                    continue
                data["date"].append(submitted_date)
                data["cities"].append(int(words[1]))
                data["url"].append(words[2])

        return pd.DataFrame(data)
