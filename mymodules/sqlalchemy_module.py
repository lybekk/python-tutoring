"""WORK IN PROGRESS
This project uses the official SQLAlchemy version
    https://www.sqlalchemy.org/
Flask has its own version of SQLalchemy
    https://flask-sqlalchemy.palletsprojects.com/en/2.x/
"""
from sqlalchemy import create_engine, MetaData
from mymodules.config import Config


class DatabaseSQLAlchemy:
    """Instantiates a class object for interacting with either a SQLite or MySQL instance using the SQLAlchemy ORM
    """
    def __init__(self, backend_type):
        """
        Depending on the parameter, this class will create an SQLAlchemy "engine" for either SQLite or MySQL.
        This enables us to use the engine object to get a connect() (connection object)
        or an execute() (Executes a SQL statement construct), among other methods.

        MySQL engine string syntax:
        create_engine("mysql://user:pwd@localhost/mydatabase")

        :param backend_type:
        """
        print("Work in progress")
        self.config = Config()
        if backend_type == "SQLite":
            self.engine = create_engine('sqlite:///training.db', echo=True)
        elif backend_type == "MySQL":
            self.engine = create_engine(
                f"mysql://{self.config.get_user()}:{self.config.get_password()}@{self.config.get_host()}/mydatabase",
                echo=True
            )

    def connection_test(self):
        """ Tests connection to the database
        TODO: Improve verification

        :return:
        """
        try:
            m = MetaData()
            m.reflect(self.engine)
            for table in m.tables.values():
                print(table.name)
                for column in table.c:
                    print(column.name)
        except Exception as e:
            print("SQLAlchemy connection test failed: ", str(e))
            return {
                "retry": True,
                "message": e
            }
