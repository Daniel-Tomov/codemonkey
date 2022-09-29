import random
import string
import json
import personalFunctions

userSessions = []


class sessions:
  def __init__(self, username):
    self.username = username
    
    currentTime = personalFunctions.time
    #print(currentTime)
    self.timeCreated = currentTime

    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    #print(token)
    self.token = token


  def refreshSession(self):
    for i in userSessions:
      if i.token == self.token and i.username == self.username:
        currentTime = personalFunctions.time
        self.token = currentTime

  def isActiveSession(self):
    currentTime = personalFunctions.time
    for i in userSessions:
      if i.token == self.token and i.username == self.username and i.timeCreated + 3000 < currentTime:
        return True
    return False

  def removeSession(self):
    for i in userSessions:
      if i.token == self.token and i.username == self.username:
        userSessions.remove(i)

def isSession(token):
  if token == None:
    return False

  for i in userSessions:
    if i.token == token:
      return True

  print("Cookie " + token + " is not in the list")
  return False

def getSession(token):
  if token == None:
    return False

  for i in userSessions:
    if i.token == token:
      return i


def removeInactiveSessions():
  currentTime = personalFunctions.time
  for i in userSessions:
    # Remove sessions that have not been refreshed for at least 30 minutes
    if i.timeCreated > (currentTime + 3000):
      print('removed ' + i.username)
      userSessions.remove(i)