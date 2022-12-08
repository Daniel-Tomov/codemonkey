from datetime import datetime, timedelta
import hashlib
import base64
import subprocess
import os
from os import listdir
from os.path import isfile, join
import threading
from time import sleep as functionSleep

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

def timeout(thread):
  # Stop the thread
  exit(0)
  # Return the "timed out" message
  return "timed out"

def runCodeWithThread(inputCode, cookie):
  thread = threading.Thread(target=runCode, args=(inputCode, cookie))
  # Start the thread
  thread.start()
  # Create a timer to interrupt the thread after 5 seconds
  timer = threading.Timer(5, timeout, args=(thread,))
  # Start the timer
  timer.start()
  # Wait for the thread to finish or be interrupted by the timer
  thread.join()

  output, error = runCode(inputCode=inputCode, cookie=cookie)
  print(f'{output}         {error}')

  if error == 1:
    return [error, 1]
  else:
    return [output, 0]

  # If the thread is still alive, return the output of runCode
  if thread.is_alive():
    return runCode(inputCode=inputCode, cookie=cookie)


  

def runCode(inputCode, cookie):
  file = open("programRuns/" + cookie + ".py", 'w')
  file.write(inputCode)
  file.close()

  args = ['python3', 'programRuns/' + cookie + ".py"]
  proc = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  output, error = proc.communicate()

  #print(process.communicate(), output, error)
  
  if error.decode('utf-8') != '':
    return [error.decode('utf-8'), 1]
  else:
    return [output.decode('utf-8'), 0]
  #stdout = process.communicate()[0].decode('utf-8')
  #print(stdout)
  
  return "Please try again"


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
