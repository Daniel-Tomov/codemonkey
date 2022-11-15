from datetime import datetime, timedelta
import hashlib
import base64
import subprocess
import os
from os import listdir
from os.path import isfile, join

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
  
  process = subprocess.Popen(['python3', 'programRuns/' + cookie + ".py"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  output, error = process.communicate()

  #print(process.communicate(), output, error)
  
  if error.decode('utf-8') != '':
    return error.decode('utf-8')
  else:
    return output.decode('utf-8')
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

'''
def expireTime(inputTime):
  hours = int(str(inputTime)[0:2])
  minutes = int(str(inputTime)[2:4])
  seconds = int(str(inputTime)[4:len(str(inputTime))])
  
  print(f'{hours}    {minutes}   {seconds}   {inputTime}')
  if minutes > 29:
    minutes = 60 + (minutes - 30)
    hours = hours - 1
    #print(f'{hours}   {minutes}')
    
  if hours >= 24:
    hours = "00"

  if len(str(minutes)) == 1:
    minutes = '0' + str(minutes)
  
  if len(str(seconds)) == 1:
    seconds = '0' + str(seconds)
  convertedTime = int(str(hours) + str(minutes) + str(seconds))

  while len(str(convertedTime)) < 6:
    convertedTime = "0" + str(convertedTime)
  return convertedTime


def convertTime(inputTime):
  hours = int(str(inputTime)[0:2])
  minutes = int(str(inputTime)[2:4])
  seconds = int(str(inputTime)[4:len(str(inputTime))])
  
  print(f'{hours}    {minutes}   {seconds}   {inputTime}')
  if minutes < 30:
    minutes = 60 + (minutes - 30)
    hours = hours - 1
    #print(f'{hours}   {minutes}')
    
  if hours >= 24:
    hours = "00"

  if len(str(minutes)) == 1:
    minutes = '0' + str(minutes)
  
  if len(str(seconds)) == 1:
    seconds = '0' + str(seconds)
  convertedTime = int(str(hours) + str(minutes) + str(seconds))

  while len(str(convertedTime)) < 6:
    convertedTime = "0" + str(convertedTime)
  return convertedTime
'''