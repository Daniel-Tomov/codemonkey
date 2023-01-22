import pickle
import yml

# define the completions dictionary
# the use of a dictionary is best because the individual instances of the completions class will be referenced by a user's UID
completions = {}

class completion:
  def __init__(self, uid):
    self.uid = uid
    # using a dictionary is best because the different challengeIDs can be used to quickly get the completion status of a question and the code the user has for that question
    self.completion = {}
    completions[uid] = self.completion

  def addCompletion(self, challID):
    self.completion[challID][0] = "complete"
  
  def removeCompletion(self, challID):
    self.completion[challID][0] = "uncomplete"

def getCompletion(uid):
  return completions[uid]

# save all user completions to the completions.pickle database
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
    # load all user from the completions.pickle database
    with open("completions.pickle", "rb") as f:
      completions = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)

# if the challenges.yaml file was updated, automatically add the updated challenges to the user's completion dictionary.
def addNewCompletions():
  data = yml.data
  for uid in completions:
    for name in data:
      for i in data[name]['page']:
        if 'question' in i:
          if data[name]['page'][i]['chal_id'] in completions[uid]:
            continue
          else:
            completions[uid][str(data[name]['page'][i]['chal_id'])] = ["", ""]

# load completions from the database. used only on startup
loadCompletions()
