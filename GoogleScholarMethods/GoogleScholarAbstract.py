import datetime


class GoogleScholarAbstract:
    # Get new publications and save them in the local filesystem, returning a dictionary with new file addresses as
    # keys and the number of citations as values
    def getNewPublications(self,
                           from_date: datetime.date,
                           to_date: datetime.date,
                           query: str) -> dict:
        pass