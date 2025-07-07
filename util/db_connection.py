import mysql.connector
import configparser
import os

def get_connection():
    config = configparser.ConfigParser()
    base_path = os.path.dirname(os.path.dirname(__file__))
    config.read(os.path.join(base_path, "config", "config.ini"))

    db_config = {
        "host": config.get("mysql", "host"),
        "port": config.getint("mysql", "port"),
        "user": config.get("mysql", "user"),
        "password": config.get("mysql", "password"),
        "database": config.get("mysql", "database"),
    }

    return mysql.connector.connect(**db_config)
