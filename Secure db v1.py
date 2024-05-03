import bcrypt
import time
import sqlite3
import os


class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def encryption(self):
        salt = bcrypt.gensalt(rounds=15, prefix=b'2a')
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def check_username(username):
        file_path = "user.db"
        if os.path.exists(file_path):
            pass
        else:
            conn = sqlite3.connect("user.db")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE user (
                username text,
                password blob
                )""")
        conn = sqlite3.connect("user.db")
        cur = conn.cursor()
        sql = "SELECT COUNT(*) FROM user WHERE username =?"
        check_user = cur.execute(sql, (username,))
        count = cur.fetchone()[0] > 0
        if count == True:
            print("you already register in our program")
            exit()

    def storge(username, hashed_password):
        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        sql = """INSERT INTO user VALUES (?, ?)"""
        cur.execute(sql, (username, hashed_password))
        conn.commit()
        conn.close()
        print('down')

    def log_in(username, password, wrong_time):
        if wrong_time < 3:
            conn = sqlite3.connect('user.db')
            cur = conn.cursor()
            sql = ("SELECT * FROM user WHERE username =?")
            check_user = cur.execute(sql, (username,))
            if check_user == True:
                hashed_password = (cur.fetchone()[1])
                result = bcrypt.checkpw(password.encode(), hashed_password)
                if result == True:
                    print("Welcome %s" % (username))
                    return True
                else:
                    print("username or password was wrong")
            else:
                print("username or password was wrong")
        else:
            print("you tring too much please give some break")
            exit()

    def chech_passwords(password):
        if len(password) <= 8:
            print(
                "your password is too short (8 charcter )please choice a betther password ")
        else:
            has_letters = False
            has_numbers = False
            for char in password:
                if char.isalpha():
                    has_letters = True
                elif char.isdigit():
                    has_numbers = True
            if not has_letters or not has_numbers:
                print("Password is too weak. It must contain both letters and numbers.")
                return has_letters and has_numbers
            else:
                return True


while True:

    choice = input("welcome do you want log-in or register ??:")
    allowed_for_reg = ["register", "reg", "sign", "signin", "sign_in"]
    allowed_for_log = ["login", "log", "log_in", "log in", "in"]
    choice = choice.lower()
    if choice in allowed_for_reg:
        username = input('Give me your username: ')
        user.check_username(username)
        while True:
            password = input('Give me your password: ')
            check_up = user.chech_passwords(password)
            if check_up == True:
                break
        hashed_password = user.encryption(password)
        user.storge(username, hashed_password)
        break

    elif choice in allowed_for_log:
        wrong_time = 0
        while True:
            username = input('Give me your username: ')
            password = input('Give me your password: ')
            result = user.log_in(username, password, wrong_time)
            if result == True:
                break
            else:
                wrong_time += 1
        break
    else:
        print('input wrong')
