#    PythonStreamDeck, a control panel for OBS in html using obs-websocket and simpleobsws
#    Copyright (C) 2022  Daniel Tomov


import yaml
from yaml.loader import SafeLoader

items = []
rawChallengesData = open('challenges.yaml', 'r').read()
data = yaml.load(open('challenges.yaml'), Loader=SafeLoader)
#print(data)


for item in data:
  items.append([item, data[item]['name'], data[item]['text'], [i for i in data[item]['page']]])

#print(items)