import personalFunctions

accounts = []

#### ADDING AND REMOVING ACCOUNTS TO AND FROM ARRAY ####
def addAccount(username, password):
  global accounts
  
  # need to hash password
  accounts.append([username, personalFunctions.encrypt(password)])
    
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
    accounts.append(i.split(','))

def saveAccounts():
  accountsTXT = open('accounts.txt', 'w')
  accountsTXT.write(accounts)