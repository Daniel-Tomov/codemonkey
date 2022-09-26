accounts = []


def addAccount(username, password):
  global accounts
  
  # need to hash password
  accounts.append([username, password])
    
def removeAccount(username, password):
  global accounts

  for i in accounts:
    i.remove([username, password])
    
    
def getAccounts():
  global accounts
  accountsTXT = open('accounts.txt', 'r').read().split('\n')

  for i in accountsTXT:
    accounts.append(i.split(','))
    

def saveAccounts():
  accountsTXT = open('accounts.txt', 'w').read().split('\n')
  accountsTXT.write(accounts)