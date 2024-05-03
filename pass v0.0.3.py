from fileinput import filename
from unittest import result
import bcrypt
import time
import os


def check_file(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass


def write_to_file(username, hashed_password, filename):
    test = ":"
    test = test.encode("utf-8")
    with open(filename, "wb") as file:
        file.write(username)
        file.write(test)
        file.write(hashed_password)


def check_user_name(username, filename):
    with open(filename, 'r') as f:
        for line in f:
            existing_username = line.strip().split(':')[0]
            if existing_username == username:
                return True
    return False


def signin():
    while True:
        username = input('give me a username: ')
        username = username.encode('utf-8')
        filename = "/home/crow/Documents/databess"
        file_path = '/home/crow/Documents/databess'
        check_file(file_path)
        if not check_user_name(username, filename):
            password = input("give me a password: ")
            hashed_password = password_encryption(password)
            write_to_file(username, hashed_password, filename)
            print("account create successfuly")
            break
        else:
            print("this username existed try another one")


def password_encryption(password):
    password = b'password'
    salt = bcrypt.gensalt(rounds=15, prefix=b'2a')
    hashed_password = bcrypt.hashpw(
        password, salt)
    return hashed_password


def check_password(result, entered_password):
    bcrypt.checkpw(result.encode, entered_password)


def find_user(username, filename):
    with open(filename, 'rb') as file:
        data = file.read()
        for line in file:
            separator = ":".encode('utf-8')
            saved_username, separator, saved_password = data.split(separator)
            if username == saved_username:
                return saved_password
        return "username not find"


def log_in():
    username = input("Enter a username: ")
    username = username.encode(
    )
    print(username)
    filename = "/home/crow/Documents/databess"
    result = find_user(username, filename)
    if result:
        entered_password = input("Enter your password: ")
        entered_password = entered_password.encode("utf-8")
        print(result, entered_password)
        check_password(result, entered_password)
        if check_file:
            print("Password is correct")
        else:
            print("Password is incorrect")
    else:
        print('username not find')


while True:
    choice = input('welcome to this app \n sign in or log in ??: ')
    if choice.lower() == 'sign in' or choice.lower() == "signin":
        signin()
        print('you register successfuly now try login')
        break
    elif choice.lower() == 'login' or choice.lower() == 'log in':
        log_in()
        break
    else:
        log_in()
