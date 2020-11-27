import pathlib
import configparser


class Config:
    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_file_path = pathlib.Path(__file__).parent.absolute().parent.absolute().joinpath("config.ini")

        if self.config_file_path.is_file():
            self.load()
        else:
            self.config_parser['DEFAULT'] = {
                "database_module_choice": "SQLite",
            }
            self.config_parser['MySQL'] = {
                "host": "localhost",
                "username": "",
                "password": "",
            }
            self.config_parser['SQLAlchemy'] = {}
            self.save()

    def get_user(self):
        value = self.config_parser.get(self.db(), "user")
        if value:
            return value
        else:
            return value

    def get_password(self):
        value = self.config_parser.get(self.db(), "password")
        return value

    def get_host(self):
        return self.config_parser.get(self.db(), "host")

    def db(self):
        """
            Shorthand for self.get_database_module_choice.
            Used in server.py db object
        """
        value = self.config_parser.get("DEFAULT", "database_module_choice")
        return value

    def set_database_module(self, db_backend):
        try:
            self.config_parser['DEFAULT']["database_module_choice"] = db_backend
            self.save()
            return "Set database module OK"
        except Exception as e:
            print("Error when setting database_module", e)
            return "Setting database module failed" + str(e)

    def get_database_module_choice(self):
        """ chooses database module """
        value = self.config_parser.get("DEFAULT", "database_module_choice")
        return value

    def save_credentials(self, username, password):
        if self.db() == "SQLite":
            return
        self.config_parser[self.db()]["username"] = username
        self.config_parser[self.db()]["password"] = password
        self.save()

    def load(self):
        self.config_parser.read(self.config_file_path)

    def save(self):
        with open(self.config_file_path, 'w') as configfile:
            self.config_parser.write(configfile)
        self.load()
