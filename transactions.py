import get_connection
import logging

logging.basicConfig(filename="app.log", level=logging.INFO, filemode="w")


class BalanceTransactions:

    def __init__(self):
        self.con = get_connection.get_con()
        self.cursor = self.con.cursor()
        self.acc_num = None
        self.balance = None
        self.attempt = 0

    def check_account(self):
        try:
            while self.attempt <= 3:
                self.acc_num = int(input("enter account number: "))
                query = (
                    "SELECT acc_number, balance FROM balance_info WHERE acc_number =%s "
                )
                self.cursor.execute(
                    query,
                    [
                        self.acc_num,
                    ],
                )
                row = self.cursor.fetchone()
                if row:
                    self.balance = row[1]
                    return self.acc_num, self.balance, self.attempt
                else:
                    if self.attempt < 3:
                        print(f"wrong acc_number. {2 - self.attempt} attempt left.")
                        self.attempt += 1
                    if self.attempt == 3:
                        print("Three failed attempts.")
                        return self.attempt
        except Exception:
            logging.error("error in account checking")
            return None

    def balance_check(self):
        self.check_account()
        if self.attempt == 3:
            return "your operation is aborted!!"
        else:
            return self.balance

    def view_balance(self):
        self.check_account()
        if self.attempt < 3:
            try:
                print(f"your current balance is £{self.balance}")
            except Exception:
                logging.exception("fault in viewing balance")
        else:
            print("operation aborted")

    def deposite(self):
        self.check_account()
        if self.attempt != 3:
            try:
                while True:
                    amount = float(input("enter amount to deposite: "))
                    if amount <= 0:
                        print("invalid amount to deposite. \nplease enter again")
                    else:
                        new_blc = amount + float(self.balance)
                        query = (
                            "UPDATE balance_info SET balance = %s WHERE acc_number = %s"
                        )
                        self.cursor.execute(query, [new_blc, self.acc_num])
                        self.con.commit()
                        print(f"money deposited! new balance is  £{new_blc}")
                        break
            except Exception:
                logging.exception("error in deposite")
        else:
            print("operation aborted.")

    def check_input(self):
        data = input('Or "exit" to exit: ')
        try:
            amount = float(data)
            exit_op = ""
            return amount, exit_op
        except:
            exit_op = data.lower()
            amount = None
            return amount, exit_op

    def withdraw_logic(self):
        amount, exit_op = self.check_input()
        while True:
            if exit_op == "exit":
                print("operation cancelled")
                break
            elif amount <= 0:
                print(
                    f'invalid amount to withdraw {amount}!!!\nplease enter again or enter "exit" to exit'
                )
            elif amount > float(self.balance):
                print(
                    'you donot have enough balance!\n please try again or enter "exit" to exit'
                )
            else:
                query = "UPDATE balance_info SET balance = %s WHERE acc_number = %s"
                new_blc = float(self.balance) - amount
                self.cursor.execute(query, [new_blc, self.acc_num])
                self.con.commit()
                print(f"money withdraw")
                break

    def withdraw(self):
        self.check_account()
        if self.attempt != 3:
            try:
                print("enter amount to withdraw")
                while True:
                    amount, exit_op = self.check_input()
                    if exit_op == "exit":
                        print("operation cancelled")
                        break
                    elif amount <= 0:
                        print(
                            f"invalid amount to withdraw {amount}!!!\nplease enter again "
                        )
                    elif amount > float(self.balance):
                        print("you donot have enough balance!\n please try again")
                    else:
                        query = (
                            "UPDATE balance_info SET balance = %s WHERE acc_number = %s"
                        )
                        new_blc = float(self.balance) - amount
                        self.cursor.execute(query, [new_blc, self.acc_num])
                        self.con.commit()
                        print("withdraw successful")
                        break
            except Exception:
                logging.exception("error in withdrawing")
        else:
            print("operation aborted")

    def transfer_balance(self):
        print("receipents account details")
        self.check_account()
        if self.attempt != 3:
            receipent_acc = self.acc_num
            receipent_blc = float(self.balance)
            print("senders details.")
            self.check_account()
            if self.attempt != 3:
                print("enter amount to transfer ")
                try:
                    while True:
                        amount, exit_op = self.check_input()
                        if exit_op == "exit":
                            print("operation cancelled")
                            break
                        elif amount <= 0:
                            print(
                                f"invalid amount to transfer {amount}!!!\nplease enter again "
                            )
                        elif amount > float(self.balance):
                            print("you donot have enough balance!\n please try again")
                        else:
                            withdraw = "UPDATE balance_info SET balance = %s WHERE acc_number = %s"
                            sender_blc = float(self.balance) - amount
                            deposite = "UPDATE balance_info SET balance = %s WHERE acc_number = %s"
                            receiver_new_blc = receipent_blc + amount
                            self.cursor.execute(withdraw, [sender_blc, self.acc_num])
                            self.cursor.execute(
                                deposite, [receiver_new_blc, receipent_acc]
                            )
                            self.con.commit()
                            print("transfer successful")
                            break
                except Exception:
                    logging.exception("error in withdrawing")
            else:
                print("operation aborted")
        else:
            print("operation aborted")

    def close_connection(self):
        self.con.close()
