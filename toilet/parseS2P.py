#!/usr/bin/env python
import csv
import sys
import datetime
import json
import requests
from requests.auth import HTTPBasicAuth

class Pooper(dict):
   def __init__(self, attributes,atrbMap):
      self['name'] = attributes[atrbMap['name']]
      self['lat'] = attributes[atrbMap['lat']]
      self['lng'] = attributes[atrbMap['lon']]
   def stringify(self):
      return self.name + " , " + self.lat +  " , " + self.lng 

def main(args):
   peeFile = open(args[1])
   firstLine = peeFile.next().split(',')
   atrbMap = dict(enumerate(firstLine))
   atrbMap = {v:k for k,v in atrbMap.items()}
   #print atrbMap
   peeReader = csv.reader(peeFile, dialect='excel')
   restrooms = []
   for line in peeReader:
      pooper = Pooper(line, atrbMap)
      restrooms.append(pooper)
   addToilets(restrooms)

def addToilets(poopers):   
   URL = 'http://127.0.0.1:8000/'
   #
   client = requests.session()
   client.get(URL)
   csrftoken = client.cookies['csrftoken']
   cookies = {'cookies' : {'csrftoken' : csrftoken}}
   #
   ## Retrieve the CSRF token first
   #client.get(URL)  # sets cookie
   #csrftoken = client.cookies['csrftoken']
   #
   #login_data = dict(username=, password=PASSWORD, csrfmiddlewaretoken=csrftoken, next='/')
   #r = client.post(URL, data=login_data, headers=dict(Referer=URL))
   #cookies = dict(csrftoken=response.cookies['csrftoken'])
   #print cookies
   response = requests.post(URL + 'api/user/create/', data=json.dumps({ 'username': 'Safe2pee', 'password' : 'peepee667', 'email':'whoknows@safe2pee.org'}),headers={'X-CSRFToken' : csrftoken, 'dataType' : 'application/json', 'Referer' : URL + 'api/user/create/', 'Origin' : URL, 'Host' : '127.0.0.1:8000'})
   print response.text
   #response = requests.post('http://127.0.0.1:8000/api/user/login/', data = json.dumps({'username': 'Safe2pee', 'password' : 'peepee667'}))
   #for pooper in poopers:
   #   try:
   #      print json.dumps(pooper)
   #      r = requests.post('http://127.0.0.1:8000/api/toilet/create/', auth=HTTPBasicAuth('Safe2pee', 'peepee667'), data=json.dumps(pooper)) 
   #   except UnicodeDecodeError:
   #      continue

   
if __name__ == "__main__":
   main(sys.argv)
