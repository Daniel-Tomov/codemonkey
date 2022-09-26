from datetime import datetime
import random
import string
import json

userSessions = []


class sessions:
  def __init__(self, username):
    self.username = username
    
    currentTime = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
    print(currentTime)
    self.timeCreated = currentTime

    token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
    print(token)
    self.token = token

    userSessions.append({'username':username, 'timeCreated':currentTime, 'token':token})


    def refreshSession(self):
      # TODO fix this \/
      self.token = ''
      for i in userSessions:
        if i['token'] == token:
          print('Token for ' + i['username'] + ' is correct')
    

def removeInactiveSessions():
  currentTime = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
  for i in userSessions:
    # Remove sessions that have not bee refreshed for at least 30 minutes
    if i['timeCreated'] > (currentTime + 3000):
      print('removed ' + i['username'])
      userSessions.remove(i)