from datetime import datetime, timedelta
import hashlib
import base64
import subprocess
import os
from os import listdir
from os.path import isfile, join
import threading
from time import sleep as functionSleep, monotonic as timer
import signal

# returns the current time but without the colons (":")
# used to track the expiration of user's sessions
def time():
  time = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
  return time

# function to hash text. Mainly used to hash passwords 
def hash(text):
  
  text = hashlib.md5(text.encode()).hexdigest()
  text = hashlib.md5(text.encode()).hexdigest()
  text = hashlib.md5(text.encode()).hexdigest()
  text = hashlib.md5(text.encode()).hexdigest()
  text = hashlib.md5(text.encode()).hexdigest()
  return text

# base64 encode text
def base64encode(input):
  return base64.b64encode(input)
# base64 decode text
def base64decode(input):
  return base64.b64decode(input)

# replacing new lines in any strings that are input with <br> for HTML
# used mainly when returning code output to the user
def replaceNewlines(input):
  return input.replace("\n", "<br>")

# get the expire time of a session 
# the input parameter is a dictionary with "hours", "minutes", and "seconds" as keys
def expireTime(timeout):
  currentTime = datetime.now()
  futureTime = currentTime + timedelta(hours=timeout['hours'], minutes=timeout['minutes'], seconds=timeout['seconds'])
  return int(str(futureTime.strftime("%H:%M:%S")).replace(':',''))
