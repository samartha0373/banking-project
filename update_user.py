import get_connection
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)


class UpdateUser:
    def __init__(self):
        self.con = get_connection.get_con()
        self.cursor = self.con.cursor()
        self.acc_num = None
        self.name = None
        self.address = None
        self.email = None
        self.attempt = 1

    def __acc_num_check(self):
        try:
            while self.attempt <= 3:
                self.acc_num = int(input("enter account number: "))
                query = """SELECT full_name,address,email FROM account_details
                            WHERE acc_number = %s """
                self.cursor.execute(
                    query,
                    [
                        self.acc_num,
                    ],
                )
                row = self.cursor.fetchone()
                if row:
                    self.name, self.address, self.email = row
                    return (
                        self.acc_num,
                        self.name,
                        self.address,
                        self.email,
                        self.attempt,
                    )
                else:
                    if self.attempt < 3:
                        print(
                            f"attempt {self.attempt} wrong! no data found!\n enter again."
                        )
                        self.attempt += 1
                    else:
                        print("3 wrong attempts. no more attempts!!!")
                        return None
        except Exception:
            logging.exception("error in account number check")
            return None

    def show_details(self):
        self.__acc_num_check()
        if self.attempt != 3:
            data = f"name: {self.name},\naddress: {self.address},\nemail: {self.email}"
            print(data)
        else:
            print("please try again.")

    def update_name(self):
        self.__acc_num_check()
        if self.attempt != 3:
            new_name = input("enter new name")
            query = "UPDATE account_details SET full_name = %s WHERE acc_number = %s"
            self.cursor.execute(query, [new_name, self.acc_num])
            self.con.commit()
            print(f"'new name updated to '{new_name}'")
        else:
            print("cannot update name, please try again!")

    def update_address(self):
        self.__acc_num_check()
        if self.attempt != 3:
            new_address = input("enter new address")
            query = """UPDATE account_details SET address = %s 
                        WHERE acc_number = %s"""
            self.cursor.execute(query, [new_address, self.acc_num])
            self.con.commit()
            print(f"new address updated to '{new_address}'")
        else:
            print("cannot update address, please try again!")

    def update_email(self):
        self.__acc_num_check()
        if self.attempt != 3:
            attempt = 1
            while attempt <= 3:
                new_email = input("enter new email: ")
                query = """SELECT * FROM account_details 
                            WHERE email = %s"""
                self.cursor.execute(
                    query,
                    [
                        new_email,
                    ],
                )
                if self.cursor.fetchone():
                    if attempt < 3:
                        print(f"""attempt {attempt} failed!!!
email already exists. use another email!""")
                        attempt += 1
                    else:
                        print("3 failed attempts.\nemail not updated.")
                        break
                else:
                    query = """UPDATE account_details SET email = %s 
                                    WHERE acc_number = %s"""
                    self.cursor.execute(query, [new_email, self.acc_num])
                    self.con.commit()
                    print(f"new email updated to '{new_email}'")
                    break

        else:
            print("cannot update email, please try again")

    def delete_account(self):
        self.__acc_num_check()
        if self.attempt != 3:
            self.cursor.execute(
                "DELETE FROM balance_info WHERE acc_number = %s",
                [
                    self.acc_num,
                ],
            )
            self.cursor.execute(
                "DELETE FROM account_details WHERE acc_number = %s",
                [
                    self.acc_num,
                ],
            )
            self.con.commit()
            print("account deleted")

    def close_con(self):
        self.con.close()
