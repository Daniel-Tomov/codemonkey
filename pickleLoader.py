import pickle

testData = [["username", "password", "standard"]]

pickleData = []

def save_object(obj):
    try:
        with open("accounts.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

def load_object(filename):
  try:
    with open(filename, "rb") as f:
      return pickle.load(f)
  except Exception as ex:
    print("Error during unpickling object (Possibly unsupported):", ex)


#save_object(testData)
pickleData = load_object("accounts.pickle")
print(pickleData)


