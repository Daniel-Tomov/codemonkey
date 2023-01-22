import pickle
import yml

# define the courseCompletions dictionary
# the use of a dictionary is best because the individual instances of the courseCompletion class will be referenced by a user's UID
courseCompletions = {}

class courseCompletion:
  def __init__(self, uid):
    # using a dictionary is best because the different page names can be used to quickly get the courseCompletion status of a question and the code the user has for that question
    tempCompletion = {}
    
    # when the instance of the object is made, use the most up-to-date information from challenges.yaml to prevent errors
    for i in yml.items:
        tempCompletion[i[0]] = ""
    courseCompletions[uid] = tempCompletion

# save the courseCompletions list to the courseCompletions.pickle database
def saveCourseCompletions():
  global courseCompletions
  try:
    with open("courseCompletion.pickle", "wb") as f:
      pickle.dump(courseCompletions, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)

# load all courseCompletions from the courseCompletions.pickle database
def loadCourseCompletions():
  global courseCompletions
  try:
    with open("courseCompletion.pickle", "rb") as f:
      courseCompletions = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)

# if the challenges.yaml file was updated, automatically add the updated modules to the user's courseCompletion dictionary.
def addNewCompletions():
  data = yml.data
  for uid in courseCompletions:
    for name in data:
      if name in courseCompletions[uid]:
        continue
      else:
        courseCompletions[uid][str(name)] = "uncomplete"


loadCourseCompletions()