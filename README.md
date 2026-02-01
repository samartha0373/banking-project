# Banking Project 🏦

**A simple, educational banking CLI in Python** — small project that demonstrates creating a MySQL-backed account system with basic operations (create account, view/update user details, deposits/withdrawals/transfers).

---

## Table of Contents

- **Features**
- **Requirements**
- **Setup**
- **Configuration**
- **Usage**
- **Logging**
- **Known issues & TODO**
- **Contributing**
- **License**

---

## 🚀 Features

- Create database and tables (`create_db.py`)
- Add customers (`add_customer.py`)
- Check / view / update user details (`update_user.py`)
- Deposit, withdraw, transfer and view balance (`transactions.py`)
- Centralized DB connection helper (`get_connection.py`)


## 🧰 Requirements

- Python 3.10+ (recommended)
- MySQL server (local or accessible)
- Python packages (see `requirements.txt`)

Notable packages from `requirements.txt`:

- `mysql-connector-python`
- `PyMySQL` (present but project currently uses `mysql-connector-python`)
- Other utility packages used for development

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## ⚙️ Configuration

The DB credentials are currently set in `get_connection.py` (host, username, password, database). For production or convenience, update that file to use environment variables or a `.env` file.

Example (recommended change to `get_connection.py`):

```python
import os
import mysql.connector

con = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    password=os.environ.get('DB_PASS', 'password'),
    database=os.environ.get('DB_NAME', 'banking_project')
)
```

> **Note:** The current code returns `None` if connection fails — to avoid downstream AttributeErrors, ensure DB connection is available or add checks before using it.


## 🧭 Database setup

Create the database and tables:

```bash
python create_db.py
```

This will create the `banking_project` database (if missing) and the `account_details` and `balance_info` tables.


## 💡 Usage

This project exposes classes you can import and use interactively or via small scripts.

Examples (interactive usage):

- Create a customer (interactive prompts):

```bash
python -c "from add_customer import AddCustomer; AddCustomer().add_customer()"
```

- View balance (interactive prompts):

```bash
python -c "from transactions import BalanceTransactions; BalanceTransactions().view_balance()"
```

- Deposit / withdraw / transfer / check account — use the `BalanceTransactions` class methods:

```python
from transactions import BalanceTransactions
bt = BalanceTransactions()
# follow interactive prompts
bt.deposite()
bt.withdraw()
bt.transfer_balance()
```

- Show or update user details via `UpdateUser`:

```python
from update_user import UpdateUser
u = UpdateUser()
u.show_details()
u.update_name()
u.update_address()
u.update_email()
```


## 📝 Logging

- Application logs are written to `app.log` (see `logging.basicConfig(...)` calls in modules).


## ⚠️ Known issues & TODO

The project is intentionally small and has a few issues that you may want to address:

- **`add_customer.generate_acc_no` / call mismatch**: `add_customer.py` defines `generate_acc_no` as a `@classmethod` but the code calls `self.__generate_acc_no()` (private name mismatch). Also the classmethod references `cls.cursor`, which doesn't exist; this needs refactoring.
- **Module side-effects**: `add_customer.py` instantiates `customer1 = AddCustomer()` at import time (and calls `print_hello()`), which is undesirable for library behavior — remove or guard with `if __name__ == '__main__':`.
- **Connection handling**: `get_connection.get_con()` returns `None` on failure; many modules assume a valid connection and will raise exceptions if `None` is returned. Consider raising a clear error or retrying.
- **Input validation & UX**: input loops and attempt counters could be simplified and made more consistent across modules.
- **No automated tests**: add unit tests for DB wrappers and logic.

Contributions or fixes for these are welcome — see below.


## 🤝 Contributing

- Fork the repo, make a new branch named `fix/description` or `feature/description`, add tests, and open a PR.
- Improve error handling, switch credentials to environment variables, and add tests for all operations.


## 📄 License

This project has no explicit license in the repository. If you want to use or share it, add a `LICENSE` file (e.g., MIT) or update it to your preferred license.


---

If you'd like, I can also:

- Add a simple `.env` support helper and update `get_connection.py` to read it ✅
- Fix the `add_customer` generation/creation bugs and add tests ✅

Tell me which one you'd like me to implement next. ✨


TODO:- 
Add Logging 
add Unit Test on top of it.
