import pickle
import yml

completions = {}

class completion:
  def __init__(self, uid):
    self.uid = uid
    self.completion = {}
    completions[uid] = self.completion

  def addCompletion(self, challID):
    self.completion[challID][0] = "complete"
  
  def removeCompletion(self, challID):
    self.completion[challID][0] = "uncomplete"

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


def addNewChallenges():
  data = yml.data
  for uid in completions:
    #print(completions[uid])
    for name in data:
      for i in data[name]['page']:
        if 'question' in i:
          #print(data[name]['page'][i])
          if data[name]['page'][i]['chal_id'] in completions[uid]:
            continue
            #print("the user already has " + str(data[name]['page'][i]['chal_id']))
          else:
            #print("added " + str(data[name]['page'][i]['chal_id']) + " to the user")
            completions[uid][str(data[name]['page'][i]['chal_id'])] = ["", ""]

loadCompletions()
