# HOLY its besen long since i have used this. Im probabaly washed
# For setup, you need to create a Userdata folder in the same directory as this script
# Inside the Userdata folder, create a file named 'user' to store user data
# Individual user data will be stored in files named after the hashed username
# If you find any security issues, please report don't report them to me i have no idea what im doing
# Copyright (c) 2025 GGX404


from cryptography.fernet import Fernet
import pickle
import hashlib
import os
import keyring
import bcrypt
import time
import getpass
data = {}
global tries, logincomplete
logincomplete = False
tries = 0
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def newuser():
    global data
    with open("./Userdata/user", "rb+") as file:
        if os.path.getsize("./Userdata/user") == 0:
            data = {}
            pickle.dump(data, file)
            file.close()
        with open("./Userdata/user", "rb") as file:
            data = pickle.load(file)
            if not isinstance(data, dict):
                data = {}

    while True:
        # Basic signup. Uses hashes for security.
        userinput = input("What do you want your username to be? ")
        newusername = hashlib.sha256(userinput.encode()).hexdigest()
        if newusername in data:
            print(bcolors.WARNING + "Your username has already been taken." + bcolors.ENDC)
            newuser()
        else:
            newpass = getpass.getpass("What will your password be? ")
            # hashed_pass = hashlib.sha256(newpass.encode()).hexdigest()
            hashed_pass = bcrypt.hashpw(newpass.encode(), bcrypt.gensalt())
            data[newusername] = {
                "password": hashed_pass,
                "lockout_until": 0,
                "failed_attempts": 0
            }
            with open(f"./Userdata/user", "wb") as f:
                pickle.dump(data, f)
            with open(f"./Userdata/{newusername}.txt", "wb") as f:
                passwords = {}
                pickle.dump(passwords, f)
                print(bcolors.OKGREEN + "New user created successfully." + bcolors.ENDC)

            break


def returnuser():
    with open("./Userdata/user", "rb") as file:
        data = pickle.load(file)
        if not isinstance(data, dict):
            data = {}
        userinput = input("What is your username? ")
        username = hashlib.sha256(userinput.encode()).hexdigest()
        if username in data:
            def passwordlogin(tries):
                user_info = data[username]
                now = time.time()
                # Check lockout
                if user_info.get("lockout_until", 0) > now:
                    wait = int(user_info["lockout_until"] - now)
                    print(bcolors.WARNING + f"Account locked. Try again in {wait} seconds." + bcolors.ENDC)
                    return
                while True:
                    newpass = getpass.getpass("What is your password? ")
                    if bcrypt.checkpw(newpass.encode(), user_info["password"]):
                        print(bcolors.OKGREEN + "You have successfully logged in." + bcolors.ENDC)
                        user_info["failed_attempts"] = 0
                        user_info["lockout_until"] = 0
                        with open("./Userdata/user", "wb") as f:
                            pickle.dump(data, f)
                        mainmenu(username)
                        global logincomplete
                        logincomplete = True
                        break
                    else:
                        print(bcolors.WARNING + "Incorrect password." + bcolors.ENDC)
                        user_info["failed_attempts"] = user_info.get("failed_attempts", 0) + 1
                        if user_info["failed_attempts"] >= 3:
                            user_info["lockout_until"] = time.time() + 300  # 5 minutes
                            with open("./Userdata/user", "wb") as f:
                                pickle.dump(data, f)
                            print(bcolors.WARNING + "Too many failed attempts. Account locked for 5 minutes."+ bcolors.ENDC)
                            exit()
                        else:
                            print(bcolors.WARNING + f"You have {3 - user_info['failed_attempts']} tries left." +bcolors.ENDC)
                            with open("./Userdata/user", "wb") as f:
                                pickle.dump(data, f)
            passwordlogin(0)
        else:
            answer = input(bcolors.WARNING + "Username not found."+bcolors.ENDC+" Would you like to create a new user? (y/n)")
            if answer.lower() == 'y':
                newuser()
            else:
                answer = input(bcolors.WARNING + "Are you sure you want to exit? (y/n)" + bcolors.ENDC)
                if answer.lower() == 'y':
                    exit()
                else:
                    returnuser()
def mainmenu(user):
    filename = "./Userdata/"+str(user) + ".txt"
    if isinstance(user, str):
        with open(filename, "rb+") as file:
            if os.path.getsize(filename) == 0:
                passwords = {}
                pickle.dump(passwords, file)
            else:
                passwords = pickle.load(file)
                if not isinstance(passwords, dict):
                    passwords = {}
                task = input("What task would you like to do?\n"+bcolors.OKCYAN+"1. Add a new login\n"+bcolors.OKGREEN+"2. view your logins\n"+ bcolors.OKBLUE + "3. delete a login\n"+bcolors.WARNING+"4. Exit"+bcolors.ENDC +"\n(1/2/3/exit):\n")
                if task == "1":
                    newpass(user)
                elif task == "2":
                    viewpass(user)
                elif task == "3":
                    deletepass(user)
                elif task.lower() == "exit":
                    print(bcolors.OKGREEN + "Exiting the program." + bcolors.ENDC)
                    exit()
                else:
                    print(bcolors.WARNING + "Invalid option. Please try again." + bcolors.ENDC)
                    mainmenu(user)
                exit()
        
    else:
        setup = input("Would you like login or signup? (login/signup): ")
        if setup.lower() == "signup":
            newuser()
            mainmenu(user)
        elif setup.lower() == "login":
            returnuser()
        else:
            print("Invalid option. Please try again.")
            mainmenu(user)
def newpass(user):
    global data
    filename = "./Userdata/"+str(user)+".txt"
    encryptkey = keyring.get_password("password_manager", user)
    with open(filename, "rb+") as file:
        passwords = pickle.load(file)
        if not isinstance(passwords, dict):
            passwords = {}
        while True:
            fernet = Fernet(encryptkey.encode())
            newlogin = input("What is the name of the program? ")
            newlogin_hash = hashlib.sha256(newlogin.encode()).hexdigest()
            if newlogin_hash in passwords:
                print("This login already exists.")
            else:
                newuser = input("What is the username for this login? ")
                newpassw = getpass.getpass("What is the password for this login? ")
                data_to_encrypt = f"{newlogin}:{newuser}:{newpassw}".encode()
                passwords[newlogin_hash] = fernet.encrypt(data_to_encrypt)
                with os.fdopen(os.open(filename, os.O_WRONLY | os.O_CREAT, 0o600), 'wb') as file:
                    pickle.dump(passwords, file)
                print(bcolors.OKGREEN+"Login added successfully."+ bcolors.ENDC)
                mainmenu(user)

def viewpass(user):
    global data
    filename = "./Userdata/"+str(user)+".txt"
    encryptkey = keyring.get_password("password_manager", user)
    with open(filename, "rb+") as file:
        passwords = pickle.load(file)
        if os.path.getsize(filename) == 0:
            passwords = {}
        if not isinstance(passwords, dict):
            passwords = {}
        showpass = input("Would you like to view all logins? (y/n): ")
        fernet = Fernet(encryptkey.encode())
        if showpass.lower() == 'y': 
            if passwords == {}:
                print(bcolors.WARNING + "No logins found." + bcolors.ENDC)
                mainmenu(user)
                return
            for encryptedinfo in passwords.values():
                decryptedinfo = fernet.decrypt(encryptedinfo).decode()
                program, username, password = decryptedinfo.split(":", 2)
                print(bcolors.OKGREEN + f"Login: {program}\n  Username: {username}\n  Password: {password}\n" + bcolors.ENDC)
            mainmenu(user)
        else:
            passname = input("What login would you like to view? ")
            passname_hash = hashlib.sha256(passname.encode()).hexdigest()
            if passname_hash in passwords:
                decryptedinfo = fernet.decrypt(passwords[passname_hash]).decode()
                program, username, password = decryptedinfo.split(":", 2)
                print(f"Login: {program}\n  Username: {username}\n  Password: {password}")
                mainmenu(user)
            else:
                print(bcolors.WARNING + "Login not found." + bcolors.ENDC)
                viewpass(user)
def deletepass(user):
    global data
    filename = "./Userdata/"+str(user)+".txt"
    with open(filename, "rb+") as file:
        passwords = pickle.load(file)
        if not isinstance(passwords, dict):
            passwords = {}
        passname = input("What login would you like to delete? ")
        passname = hashlib.sha256(passname.encode()).hexdigest()
        if passname in passwords:
            del passwords[passname]
            with open(filename, "wb") as file:
                pickle.dump(passwords, file)
            print(bcolors.OKGREEN +"Login deleted successfully." + bcolors.ENDC)
            mainmenu(user)
        else:
            print(bcolors.WARNING + "Login not found." + bcolors.ENDC)
            deletepass(user)
if logincomplete == False:
    mainmenu(0)
else:
    exit()

