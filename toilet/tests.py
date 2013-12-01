"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from toilet.models import Toilet, Flag, FlagRanking, FlagVote 
from parseS2P import main
import json
import datetime
import unittest

"""
Add Flags Equivalence Classes:
 -EQ 1: name is unique
 -EQ 2: Another flag already has this name

Retrieve Flags Equivalence Classes:
 -EQ 1: Flag with name = name exists
 -EQ 2: Flag with name = name does not exist
 
Add Restroom Equivalence Classes:
 -EQ 1: Restroom Created = Restroom Returned
 -EQ 2: Creating toilet when user is not signed in
 -EQ 3: Toilet Created with |name| < 5
 -EQ 4: Cannot retrieve coordinates for current location
 -EQ 5: Address does not exists
 

"""
class FlagTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_flag', 'foo@bar.com','bqz_qux')
        self.user.save()
        self.toilet = Toilet()
        self.toilet.name = "New toilet"
        self.toilet.date = datetime.datetime.now()
        self.toilet.creator = self.user
        self.toilet.save()
        self.client = Client()
        self.flag = Flag()
        self.flag.name = "test flag"
        self.flag.explanation = "this is a test flag"
        self.flag.save()
        
    #get flags all flags
    def test_get_flags(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/Flag/get/', {'filters' : json.dumps({})}).content)[0]
        self.assertEqual(response['pk'], self.flag.pk)
        
    #Get rankings of the flag
    def test_get_rankings(self):
        flagRanking = FlagRanking(flag=self.flag, toilet = self.toilet, up_down_vote = 0)
        flagRanking.save()
        response = json.loads(self.client.post('/api/FlagRanking/get/', {'filters' : json.dumps({'toilet' : self.toilet.pk}) }).content)[0]
        self.assertEqual(response['fields']['up_down_vote'], 0)
        self.assertEqual(response['fields']['toilet'], self.toilet.pk)
        
    #Upvoe a flag for the gien toilet
    def test_upvote_flag(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['flag'], self.flag.pk)
        self.assertEqual(response['fields']['up_down_vote'], 1)
        
    #Try to upvote the same flag on the same toilet twice
    def test_upvote_twice(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['flag'], self.flag.pk)
        self.assertEqual(response['fields']['up_down_vote'], 1)
        response = json.loads(self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['up_down_vote'], 1)
        
    #Try to upvote any flag while not logged in
    def test_upvote_not_logged_in(self):
        response = self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk})
        self.assertEqual(response.status_code, 403)
        
    #Test downvote 
    def test_downvote(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        flagRanking = FlagRanking(flag = self.flag, toilet = self.toilet, up_down_vote = 1)
        flagRanking.save()
        flagvote = FlagVote(user = self.user, flag = self.flag, toilet = self.toilet, vote = 1)
        flagvote.save()
        response = json.loads(self.client.post('/api/flag/downvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['flag'], self.flag.pk)
        self.assertEqual(response['fields']['up_down_vote'], 0)
        
    #get flags when there are no flags
    def test_get_empty_flag_set(self):
        self.flag.delete()
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/Flag/get/', {'filters' : json.dumps({})}).content)
        self.assertEqual(len(response), 0)

class ToiletTestCreate(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()
    #Create new tilet
    def test_put_toilet(self):
        self.client.login(username=self.user.username, password = 'bqz_qux')
        response = self.client.post('/api/toilet/create/', {'name' : 'test' , 'lat': 1, 'long' : 1})
        toilets = Toilet.objects.get(name='test')
        responsedict = json.loads(response.content)
        self.assertEqual(toilets.pk, responsedict[0]['pk'], "toilet created not equal to toilet returned")
        
    #Createw a new toilet while not logged in
    def test_put_toilet_not_logged_in(self):
        self.client.user = None
        response = self.client.post('/api/toilet/create/', {'data' : 'djdjdjkekle' })
        self.assertEqual(response.status_code, 401) 

    @unittest.skip("not sure if this is the right test case yet")
    def test_put_toilet_logged_in_bad_data(self):
        self.client.user = self.user
        self.client.login(username=self.user.username, password = 'bqz_qux')
        response = self.client.post('/api/toilet/create/', {'data' : 'djdjdjkekle' })
        #this may not actually be true, we should decide what to do in this case
        #there is no name specified but it still works
        self.assertEqual(response.status_code,404)

class ToiletTestGet(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()
        
    #Get tilets byt their id when the id does not exists
    def test_get_toilet_by_id_does_not_exist(self):
        response = self.client.post('/api/Toilet/get/', { 'filters' : json.dumps({'id' : 666}), 'start' : 0, 'end' : 10}) 
        self.assertEqual(json.loads(response.content), [])
        
    #get toilet using a bad filter object (toilet has no attribute foo)
    def test_get_toilet_by_bad_filter(self):
        response = self.client.post('/api/Toilet/get/', { 'filters' : {'foo' : 666}, 'start' : 0, 'end' : 10}) 
        self.assertEqual(response.status_code, 400) 
   #get all of the toilets created by a certain user
    def test_get_toilet_by_user(self): 
        toilet = Toilet()
        toilet.name = "New toilet"
        toilet.date = datetime.datetime.now()
        toilet.creator = self.user
        toilet.save()
        second_toilet = Toilet()
        second_toilet.name = "Second Toilet"
        second_toilet.date = datetime.datetime.now()
        second_toilet.creator = self.user
        second_toilet.save()
        response = self.client.post('/api/Toilet/get/', { 'filters' : json.dumps({'creator' : self.user.id}), 'start' : 0, 'end' : 10}) 
        response_list = json.loads(response.content)
        pk_list = [pk_elm for pk_elm in [ elm_list['pk']
                                        for elm_list in response_list]]
        self.assertEqual(len(pk_list), 2)
        self.assertIn(toilet.pk, pk_list)
        self.assertIn(second_toilet.pk, pk_list)
        
    #get all of the toilets created by a certain user where that user does not exists
    def test_get_toilet_by_user_not_exists(self):
        toilet = Toilet()
        toilet.name = "New toilet"
        toilet.date = datetime.datetime.now()
        toilet.creator = self.user
        toilet.save()
        second_toilet = Toilet()
        second_toilet.name = "Second Toilet"
        second_toilet.date = datetime.datetime.now()
        second_toilet.creator = self.user
        second_toilet.save()
        response = self.client.post('/api/Toilet/get/', { 'filters' : json.dumps({'creator' : 666}), 'start' : 0, 'end' : 10}) 
        response_list = json.loads(response.content)
        #this should probably be a 404 error 
        self.assertEqual(response_list, [])
               
    #get a toilet by the i of the toilet
    def test_get_toilet_by_id(self):
        toilet = Toilet()
        toilet.name = "test"
        toilet.date = datetime.datetime.now()
        toilet.lat = 1
        toilet.lng = 1
        toilet.creator = self.user
        toilet.save()
        response = self.client.post('/api/Toilet/get/', { 'filters' : json.dumps({'id' : toilet.pk }), 'start' : 0, 'end' : 10}) 
        responsedict = json.loads(response.content)
        self.assertEqual(responsedict[0]['pk'], toilet.pk, "incorrect toilet return from server")

    
