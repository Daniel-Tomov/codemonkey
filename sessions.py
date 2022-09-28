from datetime import datetime
import random
import string
import json

userSessions = []


class sessions:
  def __init__(self, username, ip):
    self.username = username
    
    currentTime = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
    #print(currentTime)
    self.timeCreated = currentTime

    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    #print(token)
    self.token = token

    self.ipAddress = ip

    userSessions.append({'username':username, 'timeCreated':currentTime, 'token':token, 'ipAddress':ip})


    def refreshSession(self, username, token):
      for i in userSessions:
        if i['token'] == token and i['username'] == username:
          print('Token for ' + i['username'] + ' is correct')

    
    def getSession(self, username, token):
      for i in userSessions:
        if i['token'] == token and i['username'] == username:
          return [i['username'], i['token']]

    def isActiveSession(self, username, token):
      currentTime = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
      for i in userSessions:
        if i['token'] == token and i['username'] == username and i['timeCreated'] + 3000 < currentTime:
          return True
      return False
    

def removeInactiveSessions():
  currentTime = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
  for i in userSessions:
    # Remove sessions that have not been refreshed for at least 30 minutes
    if i['timeCreated'] > (currentTime + 3000):
      print('removed ' + i['username'])
      userSessions.remove(i)