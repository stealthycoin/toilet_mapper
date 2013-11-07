#!/usr/bin/env python
import csv
import sys
import os
import datetime
import json
from django.core.management import call_command


class Pooper(dict):
   def __init__(self, attributes,atrbMap, toiletNum):
      self['fields'] = { 'name' : attributes[atrbMap['name']], 'lat' : attributes[atrbMap['lat']], 'lng' : attributes[atrbMap['lon']], 'numberOfReviews' : 0 , 'rating' : 0.00000, 'creator' : 1, 'date' : attributes[atrbMap['date']] }
      self['model'] = 'toilet.toilet'
      self['pk'] = toiletNum
     
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
   toiletNum = 10
   for line in peeReader:
      pooper = Pooper(line, atrbMap, toiletNum)
      toiletNum +=1 
      try:
         json.dumps(pooper)
         restrooms.append(pooper)
      except UnicodeDecodeError:
         continue

   peeFile.close()
   poopfiles = open('safetoilets.json', 'w+')
   poopfiles.write(json.dumps(restrooms))
   #addToilets(restrooms)

def addToilets(poopers):   
   URL = 'http://127.0.0.1:8000/'
   
   
if __name__ == "__main__":
   main(sys.argv)
