#!/usr/bin/env python
import csv
import sys
import os
import datetime
import json
from django.core.management import call_command
from toilet.models import Toilet
from django.contrib.auth.models import User


def main(args):
   peeFile = open(args[1])
   firstLine = peeFile.next().split(',')
   atrbMap = dict(enumerate(firstLine))
   atrbMap = {v:k for k,v in atrbMap.items()}
   #print atrbMap
   peeReader = csv.reader(peeFile, dialect='excel')
   restrooms = []
   peepee = None
   try:
      peepee = User.objects.get(username='safe2pee') 
   except User.DoesNotExist:
      peepee = User()
      peepee.username = "safe2pee"
      peepee.save()
   for line in peeReader:
      try:
        line = map(lambda x : x.decode('utf-8'), line)
      except UnicodeDecodeError:
        continue
      pooper = Toilet()
      attrs = { 'name' : line[atrbMap['name']], 'lat' : line[atrbMap['lat']], 'lng' : line[atrbMap['lon']], 'numberOfReviews' : 0 , 'rating' : 0.00000, 'creator' : peepee, 'date' : datetime.datetime.now(), 'male': True, 'female': True } 
      pooper.setattrs(attrs)
      pooper.save()
      
   
   
if __name__ == "__main__":
   main(sys.argv)
