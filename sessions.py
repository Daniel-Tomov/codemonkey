import random
import string
import personalFunctions

userSessions = []
sessionTimeout = 3000 # Thirty minutes

class sessions:
  def __init__(self, username):
    self.username = username
    
    currentTime = convertTime()
    #print(currentTime)
    self.timeCreated = currentTime
    
    self.expireTime = getExpireTime(currentTime)
    #print(self.expireTime)

    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    #print(token)
    self.token = token


  def refreshSession(self):
    self.expireTime = getExpireTime(personalFunctions.time())
    

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
    #print(f'the user {i.username} created their token at {i.timeCreated} and will expire at {expireTime}')
    if convertTime() > i.expireTime:
      print('removed the session of ' + i.username)
      userSessions.remove(i)

def getExpireTime(timeCreated):
  expireTime = timeCreated + sessionTimeout
  #print(expireTime)
  hours = int(str(expireTime)[0:2])
  minutes = int(str(expireTime)[2:4])
  if int(str(expireTime)[2:4]) >= 60:
    minutes = int(str(expireTime)[2:4]) - 60
    hours = int(str(expireTime)[0:2]) + 1
    #print(f'{hours}   {minutes}')
  if hours >= 24:
    hours = "00"
  expireTime = int(str(hours) + str(minutes) + str(expireTime)[4:len(str(expireTime))])
  return expireTime

def convertTime():
  currentTime = personalFunctions.time()
  converted = personalFunctions.time()
  if int(str(currentTime)[0:2]) == 23 and int(str(currentTime)[2:4]) > 29:
    converted = getExpireTime(personalFunctions.time()) - sessionTimeout
  #print(converted)
  return converted