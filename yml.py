import yaml
from yaml.loader import SafeLoader

# define an items list that will store some of the data from challenges.yaml
items = []

# get the raw data from challenges.yaml. Used in the textarea on the admin page
rawChallengesData = open('challenges.yaml', 'r').read().replace("\r", "")

# load the challenges.yaml with PyYAML 
data = yaml.load(open('challenges.yaml'), Loader=SafeLoader)
#print(data)

# re-read the challenges.yaml file and save any updates into the respective variables
def reloadChallenges():
  global rawChallengesData, data
  data = yaml.load(open('challenges.yaml'), Loader=SafeLoader)
  rawChallengesData = open('challenges.yaml', 'r').read().replace("\r", "")
  
  # update the items list to reflect the new challenges.yaml data
  items = []
  for item in data:
    items.append([item, data[item]['name'], data[item]['text'], [i for i in data[item]['page']]])

# write data to challenges.yaml from the admin page
def writeChallenges(input):
  file = open('challenges.yaml', 'w')
  input = input.replace("\r", "")
  file.write(input)
  file.close()