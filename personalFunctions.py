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

def time():
  time = int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))
  return time


def encrypt(password):
  password = hashlib.md5(password.encode()).hexdigest()
  password = hashlib.md5(password.encode()).hexdigest()
  password = hashlib.md5(password.encode()).hexdigest()
  password = hashlib.md5(password.encode()).hexdigest()
  password = hashlib.md5(password.encode()).hexdigest()
  return password

def base64encode(input):
  return base64.b64encode(input)
def base64decode(input):
  return base64.b64decode(input)
  

def runCode(inputCode, cookie):
  file = open("programRuns/" + cookie + ".py", 'w')
  file.write(inputCode)
  file.close()
  
  args = ['python3', 'programRuns/' + cookie + ".py"]
  #with subprocess.Popen(args=args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid) as process:
  # find cooler alternative to sigint
  with subprocess.Popen(['python3', 'programRuns/' + cookie + ".py"],stdout=subprocess.PIPE,stderr=subprocess.PIPE, preexec_fn=os.setsid) as process:
    try:
      output, error = process.communicate(timeout=4)
    except subprocess.TimeoutExpired:
      os.killpg(process.pid, signal.SIGINT) # send signal to the process group
      output, error = process.communicate()

  if error == None:
    return [output, 1]
  elif error.decode('utf-8') != '':
    return [error.decode('utf-8'), 1]
  else:
    return [output.decode('utf-8'), 0]
  


def replaceNewlines(input):
  return input.replace("\n", "<br>")

def getFiles(input):
  return [f.replace(".py", "") for f in listdir(input) if isfile(join(input, f))]

def getModifiedTime(path):
  return os.path.getmtime(path)

def deleteFile(path):
  os.system("rm -Rf " + path)

def expireTime(timeout):
  currentTime = datetime.now()
  futureTime = currentTime + timedelta(hours=timeout['hours'], minutes=timeout['minutes'], seconds=timeout['seconds'])
  return int(str(futureTime.strftime("%H:%M:%S")).replace(':',''))
