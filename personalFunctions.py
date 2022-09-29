from datetime import datetime

def time():
    return int(str(datetime.now().strftime("%H:%M:%S")).replace(':',''))