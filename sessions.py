import random
import string
import personalFunctions
import accountManager

# create the userSessions list that will store instances of the sessions class
userSessions = []

# session timeout in the for HH:MM:SS
# the : are removed so thirty minutes would be 00:30:00 -> 003000
sessionTimeout = {'hours':0, 'minutes':10, 'seconds':0} # Ten minutes

class sessions:
  def __init__(self, uid):
    self.uid = uid
    self.username = accountManager.getAccountByUID(uid).username

    # get the current time
    currentTime = personalFunctions.time()
    # set the timeCreated and refreshTime to the current time.
    # the timeCreated attribute does not change
    self.timeCreated = currentTime
    # the refreshTime attribute is the last time the user refreshed their session
    self.refreshTime = currentTime

    # set the expireTime of the session
    self.expireTime = personalFunctions.expireTime(sessionTimeout)

    # generate a random token to use for the user's session
    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    self.token = token
    
    # append this instance to the userSessions list
    userSessions.append(self)


  # method to refresh the session
  def refreshSession(self):
    # set the refreshTime to the current time
    self.refreshTime = personalFunctions.time()
    # set a new expireTime
    self.expireTime = personalFunctions.expireTime(sessionTimeout)
    
    # remove the instance from the userSessions list
  def removeSession(self):
    userSessions.remove(self)

# go through the userSessions list and find if the current session is valid
def isSession(token):
  if token == None or token == '':
    return False

  for i in userSessions:
    if i.token == token:
      # if it is valid, then refresh the session
      i.refreshSession()
      return True
  return False

# returns the instance of the session based on the input token
def getSession(token):
  if token == None or token == '':
    return None

  for i in userSessions:
    if i.token == token:
      # refresh the session because it was found to be valid
      i.refreshSession()
      return i

# function that removes inactive sessions. Found in the runPeriodically function in app.py
def removeInactiveSessions():
  # get the current time
  currentTime = personalFunctions.time()
  # iterate over the userSession list
  for i in userSessions:
    #print(f'the user {i.username} created their token at {i.timeCreated}, refreshed it at {i.refreshTime} and will expire at {i.expireTime}    the current time is {currentTime}')
    
    # Remove sessions that have not been refreshed for at least 30 minutes
    if currentTime > i.expireTime:
      userSessions.remove(i)
