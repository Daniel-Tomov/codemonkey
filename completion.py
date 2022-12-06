import pickle

completions = {}

class completion:
  def __init__(self, uid):
    self.uid = uid
    self.completion = {}
    completions[uid:self.completion]

  def addCompletion(self, challID):
    self.completion[self.uid][challID] = "complete"
  
  def removeCompletion(self, challID):
    self.completion[self.uid][challID] = "uncomplete"

def getCompletion(uid):
  return completions[uid]




def saveCompletions():
  global completions
  try:
    with open("completions.pickle", "wb") as f:
      pickle.dump(completions, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)

def loadCompletions():
  global completions
  try:
    with open("completions.pickle", "rb") as f:
      completions = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)
