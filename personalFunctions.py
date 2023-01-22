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
  
# run user code
# the cookie is used to ensure the file being written to is unique and won't be overwritten by accident
def runCode(inputCode, cookie):
  # open the file and write the code to the file
  file = open("programRuns/" + cookie + ".py", 'w')
  file.write(inputCode)
  file.close()
  # setup some variables if the code runs longer than expected
  error = b'ERROR: Your code probably took too long to execute'
  output = b'ERROR: Your code probably took too long to execute'
  
  # setup the thread that will execute code. Have the thread capture code output and errors to send back to the user.
  with subprocess.Popen(['python3', 'programRuns/' + cookie + ".py"],stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=os.setsid) as process:
    try:
      output, error = process.communicate(timeout=4) # set a timeout of 4 seconds on the process.
    except subprocess.TimeoutExpired:
      # use various methods to ensure the user's code execution proces is KILLED
      process.send_signal(signal.SIGINT)
      os.killpg(process.pid, signal.SIGINT)
      process.send_signal(signal.SIGINT)
      process.send_signal(signal.SIGTERM)

  # if there is an error, then return an array with the second index set to 1
  # otherwise, it will be 0 and no error
  if error == None:
    return [output, 1]
  elif error.decode('utf-8') != '':
    return [error.decode('utf-8'), 1]
  else:
    return [output.decode('utf-8'), 0]
  

# replacing new lines in any strings that are input with <br> for HTML
# used mainly when returning code output to the user
def replaceNewlines(input):
  return input.replace("\n", "<br>")

# get the files in the specified directory.
def getFiles(input):
  return [f.replace(".py", "") for f in listdir(input) if isfile(join(input, f))]

# delete files at the specified path
def deleteFile(path):
  os.system("rm -Rf " + path)

# get the expire time of a session 
# the input parameter is a dictionary with "hours", "minutes", and "seconds" as keys
def expireTime(timeout):
  currentTime = datetime.now()
  futureTime = currentTime + timedelta(hours=timeout['hours'], minutes=timeout['minutes'], seconds=timeout['seconds'])
  return int(str(futureTime.strftime("%H:%M:%S")).replace(':',''))
