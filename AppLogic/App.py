import datetime

import pandas as pd

import DatabaseMethods.DatabaseMethodsAbstract as db
import GigaChainMethods.GigaChainMethodsAbstract as gch
import ArticlesMethods.SelectFilesAbstract as gsm
import ArticlesMethods.GetRawText as rtx


class App:
    database: db.DatabaseMethodsAbstract
    gigachain: gch.GigaChainMethodsAbstract
    file_getter: gsm.SelectFilesAbstract
    text_getter: rtx.GetRawText
    curr_data: pd.DataFrame

    def __init__(self,
                 database: db.DatabaseMethodsAbstract,
                 gigachain: gch.GigaChainMethodsAbstract,
                 file_getter: gsm.SelectFilesAbstract,
                 text_getter: rtx.GetRawText):
        self.database = database
        self.gigachain = gigachain
        self.text_getter = text_getter
        self.file_getter = file_getter

    def get_topics(self) -> pd.DataFrame:
        return self.database.get_all_topics()

    def get_all_data_from_year(self, year: int) -> pd.DataFrame:
        self.curr_data = self.database.extract_topics_by_year(year)
        return self.curr_data

    def get_all_data_from_month_year(self, year: int, month: int) -> pd.DataFrame:
        self.curr_data = self.database.extract_topics_by_month_year(year, month)
        return self.curr_data

    def get_all_data_from_name(self, topic: str) -> pd.DataFrame:
        self.curr_data = self.database.extract_topics_by_name(topic)
        return self.curr_data

    def add_data(self, from_date: datetime.date, to_date: datetime.date):
        articles = self.file_getter.get_new_publications(from_date, to_date)
        for index, article in articles.iterrows():
            text = self.text_getter.get_text(article["link"])
            data = self.gigachain.get_themes(text)
            print(data)
            for key in data:
                self.database.increment_topic_rate(key, data[key] * article["citations"], article["date"])