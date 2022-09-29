import personalFunctions
import numpy
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
    
def getAccounts():
  global accounts
  accountsTXT = open('accounts.txt', 'r').read().split('\n')

  for i in accountsTXT:
    if i == '':
      continue
    accounts.append(i.split(','))

def saveAccounts():
  print('saving accounts')
  file = open('accounts.txt', 'w')
  print(accounts)
  for f in accounts:
    print(f)
    file.write(f'{f[0]},{f[1]},{f[2]}\n')


#### DETECT IF ACCOUNT IS AN ADMIN ####

def isAdmin(username):
  for i in accounts:
    if i[2] == "admin" and i[0] == username:
      print(f'{username} is an admin')
      return True
  return False