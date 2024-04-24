import datetime


class DatabaseMethodsAbstract:
    # gets the dictionary with themes as keys and their scores as numerical values
    def input(self,
              values: dict,
              publication_date: datetime.date):
        pass