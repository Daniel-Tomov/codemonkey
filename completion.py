

completions = {}

class completion:
  def __init__(self, uid):
    self.uid = uid
    self.completion = {}
    completions[uid:self.completion]

  def addCompletion(self, challID):
    self.completion[challID] = "complete"
  
  def removeCompletion(self, challID, uid=""):
    self.completion[challID] = "uncomplete"

def getCompletion(uid):
  return completions[uid]