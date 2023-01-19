import threading
import subprocess

class customThread(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        p = subprocess.Popen('python3 VvvtpJKsmYgRDw2UfbFy.py'.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout, self.stderr = p.communicate()



def on_timeout(proc, status_dict):
  """Kill process on timeout and note as status_dict['timeout']=True"""
  # a container used to pass status back to calling thread
  status_dict['timeout'] = True
  print("timed out")
  proc.kill()
  

def runCode(inputCode, cookie):
  file = open("programRuns/" + cookie + ".py", 'w')
  file.write(inputCode)
  file.close()

  args = ['python3', 'programRuns/' + cookie + ".py"]
  proc = subprocess.Popen(args, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  status_dict = {'timeout':False}

  # trigger timout and kill process in 5 seconds
  timer = threading.Timer(5, on_timeout, (proc, status_dict))
  timer.start()
  proc.wait()
  # in case we didn't hit timeout
  timer.cancel()


myThread = customThread()
myThread.start()
myThread.join()
print(myThread.stdout.decode('utf-8'))