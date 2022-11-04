import random
import string
import personalFunctions

userSessions = []
# session timeout in the for HH:MM:SS
# the : are removed so thirty minutes would be 00:30:00 -> 003000
sessionTimeout = {'hours':0, 'minutes':10, 'seconds':0} # Thirty minutes

class sessions:
  def __init__(self, username):
    self.username = username
    
    currentTime = personalFunctions.time()
    
    self.timeCreated = personalFunctions.time()
    #print(self.timeCreated)
    
    self.expireTime = personalFunctions.expireTime(sessionTimeout)
    #print(self.expireTime)

    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    #print(token)
    self.token = token


  def refreshSession(self):
    self.expireTime = personalFunctions.expireTime(sessionTimeout)
    

  def isActiveSession(self):
    currentTime = personalFunctions.time()
    if self.expireTime > currentTime:
      self.refreshSession()
      return True
    return False

  def removeSession(self):
    userSessions.remove(self)

def isSession(token):
  if token == None or token == '':
    return False

  for i in userSessions:
    if i.token == token:
      i.refreshSession()
      return True

  #print("Cookie " + token + " is not in the list")
  return False

def getSession(token):
  if token == None or token == '':
    return None

  for i in userSessions:
    if i.token == token:
      i.refreshSession()
      return i


def removeInactiveSessions():
  currentTime = personalFunctions.time()
  for i in userSessions:
    # Remove sessions that have not been refreshed for at least 30 minutes
    print(f'the user {i.username} created their token at {i.timeCreated} and will expire at {i.expireTime}    the current time is {currentTime}')
    if currentTime > i.expireTime:
      print(i.expireTime)
      print('removed the session of ' + i.username)
      userSessions.remove(i)
