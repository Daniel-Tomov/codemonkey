#    PythonStreamDeck, a control panel for OBS in html using obs-websocket and simpleobsws
#    Copyright (C) 2022  Daniel Tomov


import yaml
from yaml.loader import SafeLoader

items = []
rawChallengesData = open('challenges.yaml', 'r').read().replace("\r", "")
data = yaml.load(open('challenges.yaml'), Loader=SafeLoader)
#print(data)


def reloadChallenges():
  global rawChallengesData, data
  data = yaml.load(open('challenges.yaml'), Loader=SafeLoader)
  rawChallengesData = open('challenges.yaml', 'r').read().replace("\r", "")

def writeChallenges(input):
  file = open('challenges.yaml', 'w')
  input = input.replace("\r", "")
  file.write(input)

for item in data:
  items.append([item, data[item]['name'], data[item]['text'], [i for i in data[item]['page']]])


#print(items)