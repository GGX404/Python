from cryptography.fernet import Fernet
import pickle
import hashlib
import os
import keyring
with open('user', 'wb+') as f:
    data = {}
    userinput = input('What do you want your username to be? ')
    newpass = input('What will your password be? ')
    newusername = hashlib.sha256(userinput.encode()).hexdigest()
    newpass = hashlib.sha256(newpass.encode()).hexdigest()
    encryptkey = Fernet.generate_key()
    keyring.set_password("password_manager", newusername, encryptkey.decode())
    data[newusername] = {
        "password": newpass,
        "lockout_until": 0,
        "failed_attempts": 0
    }
    pickle.dump(newusername, f)