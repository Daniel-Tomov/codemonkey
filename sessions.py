import random
import string
import json
import personalFunctions
import time

userSessions = []
sessionTimeout = 3000 # Thirty minutes

class sessions:
  def __init__(self, username):
    self.username = username
    
    currentTime = personalFunctions.time()
    #print(currentTime)
    self.timeCreated = currentTime

    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    #print(token)
    self.token = token


  def refreshSession(self):
    self.timeCreated = personalFunctions.time()

  def isActiveSession(self):
    currentTime = personalFunctions.time()
    if self.timeCreated + sessionTimeout < currentTime:
      return True
    return False

  def removeSession(self):
    userSessions.remove(self)

def isSession(token):
  if token == None:
    return False

  for i in userSessions:
    if i.token == token:
      return True

  #print("Cookie " + token + " is not in the list")
  return False

def getSession(token):
  if token == None:
    return False

  for i in userSessions:
    if i.token == token:
      return i


def removeInactiveSessions():
  while True:
    currentTime = personalFunctions.time()
    for i in userSessions:
      expireTime = i.timeCreated + sessionTimeout
      # Remove sessions that have not been refreshed for at least 30 minutes
      #print(f'the user {i.username} created their token at {i.timeCreated} and will expire at {expireTime}')
      if currentTime > expireTime:
        print('removed ' + i.username)
        userSessions.remove(i)
    time.sleep(10)