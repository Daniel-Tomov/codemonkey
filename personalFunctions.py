from datetime import datetime
import hashlib

def time():
    return int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))


def encrypt(password):
  password = hashlib.md5(password.encode()).hexdigest()
  return password