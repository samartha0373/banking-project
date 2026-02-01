import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)


def get_con():
    try:
        con = mysql.connector.connect(
            host="localhost",
            username="root",
            password="password",
            database="banking_project",
        )
        return con
    except Exception:
        logging.exception("error in connection")
        return None
