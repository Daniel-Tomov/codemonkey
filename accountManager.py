import personalFunctions
import numpy
import pickle
import time

accounts = []

#### ADDING, CHECKING, AND REMOVING ACCOUNTS TO AND FROM ARRAY ####
def addAccount(username, password):
  global accounts
  
  # need to hash password
  encryptedPassword = personalFunctions.encrypt(password)
  #print(f'created a new account with username {username} and password {encryptedPassword}')
  accounts.append([username, encryptedPassword, 'standard'])
    
def removeAccount(username, password):
  global accounts

  for i in accounts:
    i.remove([username, personalFunctions.encrypt(password)])


def checkAccount(username, password):
  for i in accounts:
    if i[0] == username and i[1] == personalFunctions.encrypt(password):
      return True
  return False

    
#### SAVING AND GETTING ACCOUNTS ####
    
def old_getAccounts():
  global accounts
  accountsTXT = open('accounts.txt', 'r').read().split('\n')

  for i in accountsTXT:
    if i == '':
      continue
    accounts.append(i.split(','))

def old_saveAccounts():
  file = open('accounts.txt', 'w')
  for f in accounts:
    file.write(f'{f[0]},{f[1]},{f[2]}\n')


#### DETECT IF ACCOUNT IS AN ADMIN ####

def isAdmin(username):
  for i in accounts:
    if i[2] == "admin" and i[0] == username:
      #print(f'{username} is an admin')
      return True
  return False


  #### DETECT IF ACCOUNT EXISTS ####

def accountExists(username):
  for i in accounts:
    if i[0] == username:
      return True
  return False


def saveAccounts():
  global accounts
  try:
    with open("accounts.pickle", "wb") as f:
      pickle.dump(accounts, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)

def getAccounts():
  global accounts
  try:
    with open("accounts.pickle", "rb") as f:
      accounts = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)

#old_getAccounts()
#saveAccounts()
getAccounts()