

import pickle
import random
from tkinter import messagebox, simpledialog

username = ''
def newuser():
    with open('user', 'rb+') as file:
        data = pickle.load(file)
        with open('user', 'wb+') as f:
            newusername = simpledialog.askstring(' ', 'What do you want your username to be?')
            if newusername in data:
                messagebox.showerror('', 'Your username has already been taken.')
                newuser()
            else:
                newpass = simpledialog.askstring(' ', 'What will your password be?')
                toadd = [newpass, '', 0, '']
                data[newusername] = toadd
                pickle.dump(data, f)



def getinfo(usernamegiven, passwordgiven):
    with open('user', 'rb+') as f:
        data = pickle.load(f)
        in_data = usernamegiven in data
        if in_data == True:
            global password, info
            info = data[usernamegiven]
            password = info[0]
            level = info[1]
            name = info[2]
            if password == passwordgiven:
                global newinfo
                player = simpledialog.askinteger(' ', 'Which player would you like to play in? 1: ')
                player1 = [level, name]
                newinfo = [password,]
               
                data[username] = newinfo
            else:
                retrypass = simpledialog.askstring(' ', 'Your password was incorrect. Please put the correct password in.')
                getinfo(username, retrypass)
        else:
            messagebox.showerror(' ', 'You do not have an account. You will be redirected to create a new one.')
            newuser()

def createnewplayer():
    player1 = simpledialog.askstring('','What do you want your character to be named? ')
    weaponchoice = simpledialog.askinteger(' ', 'Which gun would you like? 1: AK47 | 2: Sniper Rifle | 3: SMG')
    if weaponchoice == 1:
        weapon = 'AK47'
    elif weaponchoice == 2:
        weapon = 'Sniper'
    else:
        weapon = 'SMG'
    weaponinfo = [1, weapon]
    playerinfo = [1, weaponinfo]
    info[player1] = playerinfo

def infograb():
    newplayer = messagebox.askyesno(' ', 'Are you a new player?')
    if newplayer == True:
        newuser()
    else:
        theusername = simpledialog.askstring(' ', 'To begin, please provide your username: ')
        thepassword = simpledialog.askstring(' ', 'What is your password? ')
        getinfo(theusername, thepassword)

def getskilllevel(userlevel):
    if userlevel < 5:
        baseskill_level = 1 
        maxskill_level = 5
    elif userlevel >= 5 and userlevel < 10:
        baseskill_level = 5
        maxskill_level = 10
    elif userlevel >= 10 and userlevel < 15:
        baseskill_level = 10
        maxskill_level = 15
    elif userlevel >= 15 and userlevel < 20:
        baseskill_level = 15
        maxskill_level = 20
    elif userlevel >= 20 and userlevel < 25:
        baseskill_level = 20
        maxskill_level = 25
    elif userlevel >= 25 and userlevel < 35:
        baseskill_level = 25
        maxskill_level = 35
    else:
        baseskill_level = 35
        maxskill_level = 50
    return baseskill_level, maxskill_level

def getbottype():
    types = ['soldier', 'artillery', 'tank', 'plane', 'bomber']
    bottype = random.choice(types)
    return bottype
def specificfight():
    pass
    
def fightscene(userlevel, playername):
    base, max  = getskilllevel(userlevel)
    enemylevel = random.randint(base, max)
    print(enemylevel)
    bottype = getbottype()
    messagebox.showwarning(' ', 'A level '+enemylevel+' '+bottype+' has appeared!')
    






