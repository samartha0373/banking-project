import get_connection
import logging_file


class AddCustomer:

    def __init__(self):
        self.con = get_connection.get_con()
        self.cursor = self.con.cursor()

    def add_customer(self):
        try:
            name = input("enter full name: ")
            address = input("enter address: ")
            email = self.__email_check()
            if not email:
                print("account creation aborted.")
                return
            account_details = """
                        INSERT INTO account_details (
                        full_name, acc_number,address,email)
                        VALUES (%s,%s, %s, %s)"""
            self.cursor.execute(account_details, [name, address, email])
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            acc_number = self.cursor.fetchone()
            print("account created.")
            print(
                f"your account number is {acc_number}.\n Please note down your account number."
            )
            balance_info = """
                            INSERT INTO balance_info (
                            acc_number)
                            VALUES (%s)"""
            self.cursor.execute(
                balance_info,
                [
                    acc_number,
                ],
            )
        except Exception:
            logging_file.logging.exception("error")
        finally:
            self.con.commit()
            self.con.close()

    def __email_check(self):
        attempt = 1
        while attempt <= 3:
            email = input("enter new email: ")
            query = """SELECT * FROM account_details 
WHERE email = %s"""
            self.cursor.execute(
                query,
                [
                    email,
                ],
            )
            if self.cursor.fetchone():
                if attempt < 3:
                    print(
f"""attempt {attempt} failed!!!\nemail already exists. use another email!""")
                    attempt += 1
                else:
                    print("3 failed attempts.")
                    return None
            else:
                break
        return email
