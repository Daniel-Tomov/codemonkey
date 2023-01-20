import pickle
import yml

courseCompletions = {}

class courseCompletion:
  def __init__(self, uid):
    tempCompletion = {}
    for i in yml.items:
        tempCompletion[i[0]] = ""
    courseCompletions[uid] = tempCompletion

def saveCourseCompletions():
  global courseCompletions
  try:
    with open("courseCompletion.pickle", "wb") as f:
      pickle.dump(courseCompletions, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)

def loadCourseCompletions():
  global courseCompletions
  try:
    with open("courseCompletion.pickle", "rb") as f:
      courseCompletions = pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)

def addNewCompletions():
  data = yml.data
  for uid in courseCompletions:
    #print(courseCompletions[uid])
    for name in data:
      #print(name)
      #print(data[name])
      #print(list((courseCompletions[uid]).keys()))
      #print(name)
      if name in courseCompletions[uid]:
        continue
      else:
        #print("added " + name)
        courseCompletions[uid][str(name)] = "uncomplete"


loadCourseCompletions()