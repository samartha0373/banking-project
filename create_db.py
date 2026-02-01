import mysql.connector
import get_connection
import logging

logging.basicConfig(level=logging.ERROR)


class CreateDatabase:

    def __init__(self):
        self.con = get_connection.get_con()
        self.cursor = self.con.cursor()

    def create_db(self):
        try:
            con = mysql.connector.connect(
                host="localhost", username="root", password="password"
            )
            cursor = con.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS banking_project")
            con.commit()
        except Exception:
            logging.exception("error in connection")

    def create_tables(self):
        """creating tables for banking project"""
        try:
            account_details = """
                        CREATE TABLE IF NOT EXISTS account_details(
                        full_name VARCHAR(30) NOT NULL,
                        acc_number INT PRIMARY KEY AUTO_INCREMENT,
                        address VARCHAR(50) NOT NULL,
                        email VARCHAR(30) UNIQUE NOT NULL,
                        created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP )
                        AUTO_INCREMENT = 30380001
                        """
            balance_info = """
                        CREATE TABLE IF NOT EXISTS balance_info(
                        acc_number INT PRIMARY KEY,
                        balance DECIMAL(10,2) DEFAULT 0,
                        updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
                            FOREIGN KEY (acc_number) REFERENCES account_details(acc_number),
                            CHECK (balance BETWEEN 0 AND 99999999.99)  
                            )"""
            tables = [
                ("account_details", account_details),
                ("balance_info", balance_info),
            ]
            for name, table in tables:
                self.cursor.execute(table)
                self.con.commit()
        except Exception:
            logging.exception("error")

    def main(self):
        self.create_db()
        print("database created!")
        self.create_tables()
        print("tables created")
        self.con.close()
