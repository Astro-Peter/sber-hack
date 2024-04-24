import datetime
from abc import ABC, abstractmethod


class DatabaseMethodsAbstract(ABC):
    @abstractmethod
    def get_all_topics(self):
        pass

    @abstractmethod
    def increment_topic_rate(self, topic_name: str, rating_increment: int, rating_date: datetime.date):
        pass

    @abstractmethod
    def extract_topics_by_month_year(self, year: int, month: int):
        pass

    @abstractmethod
    def extract_topics_by_year(self, year: int):
        pass

