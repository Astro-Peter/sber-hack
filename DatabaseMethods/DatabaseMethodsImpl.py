from datetime import datetime
import psycopg2
import pandas as pd

from DatabaseMethods.DatabaseMethodsAbstract import DatabaseMethodsAbstract


class DatabaseMethods(DatabaseMethodsAbstract):
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)

    def update_topic_ratings(self, values: dict, publication_date: datetime.date):
        with self.conn.cursor() as cursor:
            for topic_name, rating in values.items():
                cursor.execute(
                    "SELECT add_topic_rating(%s, %s, %s)",
                    (topic_name, rating, publication_date)
                )
        self.conn.commit()

    def get_all_topics(self):
        query = "SELECT id, name FROM topics"
        return pd.read_sql_query(query, self.conn)

    def increment_topic_rate(self, topic_name: str, rating_increment: int, rating_date: datetime.date):
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT add_topic_rating(%s, %s, %s)",
                (topic_name, rating_increment, rating_date)
            )
        self.conn.commit()

    def extract_topics_by_month_year(self, year: int, month: int):
        query = """
            SELECT t.name, tr.rating 
            FROM topics t 
            JOIN topic_rates tr ON t.id = tr.topic_id 
            WHERE tr.year = %s AND tr.month = %s
        """
        return pd.read_sql_query(query, self.conn, params=(year, month))

    def extract_topics_by_year(self, year: int):
        query = """
            SELECT t.name, SUM(tr.rating) 
            FROM topics t 
            JOIN topic_rates tr ON t.id = tr.topic_id 
            WHERE tr.year = %s 
            GROUP BY t.name
        """
        return pd.read_sql_query(query, self.conn, params=(year,))

    def extract_topics_by_name(self, topic_name: str):
        query = """
                    SELECT t.name, tr.rating, tr.year, tr.month 
                    FROM topics t 
                    JOIN topic_rates tr ON t.id = tr.topic_id 
                    WHERE t.name = %s
                """
        return pd.read_sql_query(query, self.conn, params=(topic_name,))