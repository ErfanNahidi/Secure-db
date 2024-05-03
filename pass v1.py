import bcrypt
print('welcome to this program:')
username = input('Enter your username:')
password = input('now enter your password:')
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
deta = dict(username=username, password=hashed_password)
print(deta)
