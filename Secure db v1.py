import os
import sqlite3
import string
import time

import bcrypt


class Database:
    def __init__(self, file_pt: str) -> None:
        self.file_pt = file_pt

        if not os.path.exists(self.file_pt):
            self.conn = sqlite3.connect("user.db")
            self.__generate_db()
        else:
            self.conn = sqlite3.connect("user.db")

    def __generate_db(self) -> None:
        """Generate the tables required."""
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(
                """
                CREATE TABLE user (
                    username text,
                    password blob
                );
            """
            )

    @staticmethod
    def encrypt_pass(password: str) -> bytes:
        """Encrypt password"""
        salt = bcrypt.gensalt(rounds=15, prefix=b"2a")
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def log_in(self) -> None:
        """Login to account."""
        tries = 0

        while tries < 3:
            username = input("Enter your username > ")

            cur = self.conn.cursor()

            try:
                hashed_password: bytes = cur.execute(
                    "SELECT password FROM user WHERE username =?", (username,)
                ).fetchone()[0]
            except TypeError:
                print("User does not exist!")
                tries += 1
                continue

            password = input("Give me your password > ")

            is_valid = bcrypt.checkpw(password.encode(), hashed_password)

            if is_valid:
                print(f"Welcome {username}!")
                return

            tries += 1
            print("username or password was wrong")

        print("You're trying too much, please give some break.")

    def sign_up(self) -> None:
        username = self.__sign_up_get_username()
        password = self.__sign_up_get_password()
        self.__sign_up_insert(username, password)

    def __sign_up_get_username(self) -> str:
        """Gets a valid username without invalid characters and checks if it exists in db."""

        while True:
            username = input("Give me your username > ")

            if len(username) < 5 and len(username) > 15:
                print("Your username is must have between 5 and 15 characters.")
                continue

            if any(num in username for num in string.punctuation):
                print("Your username must not have punctuations.")
                continue

            if any(num in username for num in string.whitespace):
                print("Your username must not have whitespace.")
                continue

            cur = self.conn.cursor()
            user_count = cur.execute(
                "SELECT COUNT(*) FROM user WHERE username =?",
                (username,),
            ).fetchone()[0]

            if user_count > 0:
                print("User is already registered in our program.")

                answer = input("Wanna try again (y, n) > ").lower()
                if answer == "n":
                    # Just to jump outside when user doesn't want to register
                    raise KeyboardInterrupt

            else:
                break

        return username

    @staticmethod
    def __sign_up_get_password() -> str:
        """Gets a valid password from the user."""

        while True:
            password = input("Give me your password > ")

            if len(password) >= 8:
                if [char in string.digits for char in password].count(True) >= 4:
                    if [char in string.ascii_letters for char in password].count(True) >= 4:
                        return password
                    else:
                        print("Your password must at least have 4 letters.")
                else:
                    print("Your password must at least have 4 digits.")
            else:
                print("Your password is too short (Valid password is 8 charcters).")

    def __sign_up_insert(self, username: str, password: str):
        """Inserts the username and password to db"""
        hashed_password = self.encrypt_pass(password)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO user VALUES (?, ?);", (username, hashed_password))

        print("Sign up done!")


def main() -> None:
    print("Welcome!")

    while True:
        db = Database("user.db")

        try:
            choice = input(
                "Do you want log-in or register?? (log, reg) > "
            ).lower()
        except KeyboardInterrupt:
            print("\n\nGoodbye :)")
            exit()

        allowed_for_reg = ["register", "reg", "sign", "signin", "sign_in"]
        allowed_for_log = ["login", "log", "log_in", "log in", "in"]

        if choice in allowed_for_reg:
            try:
                db.sign_up()
            except KeyboardInterrupt:
                print("\nYou cancelled the sign up process.")

        elif choice in allowed_for_log:
            try:
                db.log_in()
            except KeyboardInterrupt:
                print("\nYou cancelled the login process.")


if __name__ == "__main__":
    main()
