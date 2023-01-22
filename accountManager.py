import personalFunctions
import pickle
import random
import string

# create array to store instances of the accountManager class
accounts = []
# used to compare preSurvey and postSurvey for completion of the respective surveys
surveyDict = {"feeling":"","pursue":""}

# definition for accountManager class
class accountManager:
  def __init__(self, username, email, password, uid="", adminStatus=False):
    self.username = username
    self.password = personalFunctions.hash(password)
    self.email = email
    self.preSurvey = {"feeling":"","pursue":""}
    self.postSurvey = {"feeling":"","pursue":""}
    self.finished = False
    self.free = 'false'

    # create a UID for the user if one was not supplied
    if uid == "":
      self.uid = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890' + "", k=50))
    else:
      self.uid = uid

    # set the admin parameter of the instance to the value of the adminStatus parameter
    self.admin = adminStatus

    # append this instance of the accountManager class to the accounts array
    accounts.append(self)
      
  # return the admin status of the user
  def isAdmin(self):
    if self.admin:
      return True
    return False

  # while this is not used anywhere, still good to have it
  def removeAccount(self):
    global accounts
    accounts.remove(self)

  
# check if the supplied username and password are a valid account
def checkAccount(username, password):
  for i in accounts:
    if i.username == username and i.password == personalFunctions.hash(password):
      return True
  return False

# returns the instance of the accountManager class that equals the supplied UID
def getAccountByUID(uid):
  global accounts
  for i in accounts:
    if i.uid == uid:
      return i
  return None

# returns the instance of the accountManager class that equals the supplied username
def getAccountByUsername(username):
  global accounts
  for i in accounts:
    if i.username == username:
      return i
  return None
# returns the instance of the accountManager class that equals the supplied email
def getAccountByEmail(email):
  global accounts
  for i in accounts:
    if i.email == email:
      return i
  return None

#### SAVING AND GETTING ACCOUNTS ####
def saveAccounts():
  # use the accounts list defined above
  global accounts
  try:
    # save the current status of the accounts list to the accounts.pickle database
    with open("accounts.pickle", "wb") as f:
      pickle.dump(accounts, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)

def loadAccounts():
  # use the accounts list defined above
  global accounts
  try:
     # load the accounts.pickle database and save it to the accounts list
    with open("accounts.pickle", "rb") as f:
      accounts = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)
    #old_getAccounts()

# load the accounts. Only used on startup
loadAccounts()