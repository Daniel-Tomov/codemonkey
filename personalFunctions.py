from datetime import datetime
import hashlib

def time():
    return int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))


def encrypt(password):
  key = hashlib.sha256(password).digest()
  return key
