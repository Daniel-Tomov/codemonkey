import pickle
from yml import items

courseCompletions = {}

class courseCompletion:
  def __init__(self, uid):
    tempCompletion = {}
    for i in items:
        print(i[0])
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


loadCourseCompletions()
