import os
import logging
import pyodbc

from dotenv import load_dotenv

class DbService:
    connection = None
    cursor = None

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()
        self.server = os.environ.get("DB_SERVER")
        self.db_name = os.environ.get("DB_NAME")
        self.user = os.environ.get("DB_USER")
        self.password = os.environ.get("DB_PWD")
        if self.connection is None:
            self.connect()

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                "DRIVER={SQL Server};SERVER="
                + self.server
                + ";DATABASE="
                + self.db_name
                + ";Trusted_Connection=yes;"
            )

            self.cursor = self.connection.cursor()
        except Exception as e:
            logging.error("Error connecting to the database:", e)
            raise

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor
        except Exception as e:
            logging.error("Error executing query:", e)
            self.connection.rollback()
            raise

    def execute_many(self, query, params=None):
        try:
            self.cursor.executemany(query, params or ())
            self.connection.commit()
            return self.cursor
        except Exception as e:
            logging.error("Error executing query:", e)
            self.connection.rollback()
            raise

    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()

            self.cursor.execute("SELECT @@IDENTITY AS LastID;")
            last_id = self.cursor.fetchone().LastID

            return True, last_id  
        except Exception as e:
            error_message = "Error executing query: {}".format(e)
            logging.error(error_message)
            self.connection.rollback()
            return False, error_message  

    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            data = self.cursor.fetchall()
            return data or None
        except Exception as e:
            logging.error("Error fetching data:", e)
            raise

    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            data = self.cursor.fetchone()
            return data or None
        except Exception as e:
            logging.error(f"Error fetching data: {query} ", e)
            raise

    def close(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self.close()
