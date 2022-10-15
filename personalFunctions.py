from datetime import datetime
import hashlib
import base64
import subprocess
import os
from os import listdir
from os.path import isfile, join

def time():
    return int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))


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
  os.system("echo '" + inputCode + "' > ./programRuns/" + cookie + ".py")
  process = subprocess.Popen(['python3', 'programRuns/' + cookie + ".py"], stdout=subprocess.PIPE)
  stdout = process.communicate()[0].decode('utf-8')
  #print(stdout)
  
  return stdout


def replaceNewlines(input):
  return input.replace("\n", "<br>")

def getFiles(input):
  return [f for f in listdir(input) if isfile(join(input, f))]

def getModifiedTime(path):
  return os.path.getmtime(path)

def deleteFile(path):
  os.system("rm -Rf " + path)