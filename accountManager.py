import personalFunctions
import pickle
import random
import string

accounts = []


class accountManager:
  def __init__(self, username, email, password, uid="", adminStatus=False):
    self.username = username
    self.password = personalFunctions.encrypt(password)
    self.email = email

    if uid == "":
      self.uid = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890' + "", k=50))
    else:
      self.uid = uid

    if adminStatus:
      self.admin = True
    else:
      self.admin = False

    if username == "Daniel":
      self.admin = True

    accounts.append(self)
      
  def isAdmin(self):
    if self.admin:
      return True
    return False

  def removeAccount(self):
    global accounts
    accounts.remove(self)

  
def checkAccount(username, password):
  for i in accounts:
    #print(f'{i.username}   {i.password} ||    {username}  {password}')
    if i.username == username and i.password == personalFunctions.encrypt(password):
      return True
  return False

def getAccountByUID(uid):
  global accounts
  for i in accounts:
    if i.uid == uid:
      return i
  return None

def getAccountByName(username):
  global accounts
  for i in accounts:
    if i.username == username:
      return i
  return None
    
#### SAVING AND GETTING ACCOUNTS ####
    
def old_getAccounts():
  global accounts
  accountsTXT = open('accounts.txt', 'r').read().split('\n')
  return None
  for i in accountsTXT:
    if i == '':
      continue
    else:
      username = i.split(',')[0]
      uid = i.split(',')[1]
      password = i.split(',')[2]
      adminStatus = i.split(',')[3]
      accounts.append(accountManager(username, password))
  
def old_saveAccounts():
  file = open('accounts.txt', 'w')
  for f in accounts:
    file.write(f'{f[0]},{f[1]},{f[2]}\n')


  #### DETECT IF ACCOUNT EXISTS ####

def accountExistsByUsername(username):
  for i in accounts:
    if i.username == username:
      return True
  return False

def accountExistsByEmail(email):
  for i in accounts:
    if i.email == email:
      return True
  return False


def saveAccounts():
  global accounts
  try:
    with open("accounts.pickle", "wb") as f:
      pickle.dump(accounts, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)

def loadAccounts():
  global accounts
  try:
    with open("accounts.pickle", "rb") as f:
      accounts = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)
    old_getAccounts()

#old_getAccounts()
#saveAccounts()
loadAccounts()