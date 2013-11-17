"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from toilet.middletier import listing
from django.test.client import Client
from django.contrib.auth.models import User
from toilet.models import Toilet, Flag, FlagRanking, FlagVote 
from parseS2P import main
import json
import datetime
import unittest

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
        
    def test_get_flags(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/flag/retrieve_flags/', {}).content)[0]
        self.assertEqual(response['pk'], self.flag.pk)

    def test_upvote_flag(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['pk'], self.flag.pk)
        self.assertEqual(response['fields']['up_down_vote'], 1)

    def test_upvote_twice(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['up_down_vote'], 1)
        response = json.loads(self.client.post('/api/flag/upvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['up_down_vote'], 1)

    def test_downvote(self):
        self.client.login(username=self.user.username, password ='bqz_qux')
        flagRanking = FlagRanking(flag = self.flag, toilet = self.toilet, up_down_vote = 1)
        flagRanking.save()
        flagvote = FlagVote(user = self.user, flag = self.flag, toilet = self.toilet, vote = 1)
        flagvote.save()
        response = json.loads(self.client.post('/api/flag/downvote/', {'toilet_pk' : self.toilet.pk, 'flag_pk' : self.flag.pk}).content)[0]
        self.assertEqual(response['fields']['up_down_vote'], 0)

    def test_get_empty_flag_set(self):
        self.flag.delete()
        self.client.login(username=self.user.username, password ='bqz_qux')
        response = json.loads(self.client.post('/api/flag/retrieve_flags/', {}).content)
        self.assertEqual(len(response), 0)



        


        

    def test_upvote(self):
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()



class ToiletTestCreate(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()

    def test_put_toilet(self):
        self.client.login(username=self.user.username, password = 'bqz_qux')
        response = self.client.post('/api/toilet/create/', {'name' : 'test' , 'lat': 1, 'long' : 1})
        toilets = Toilet.objects.get(name='test')
        responsedict = json.loads(response.content)
        self.assertEqual(toilets.pk, responsedict[0]['pk'], "toilet created not equal to toilet returned")
 
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

    def test_get_toilet_by_id_does_not_exist(self):
        response = self.client.post('/api/Toilet/get/', { 'filters' : json.dumps({'id' : 666}), 'start' : 0, 'end' : 10}) 
        self.assertEqual(json.loads(response.content), [])

    def test_get_toilet_by_bad_filter(self):
        response = self.client.post('/api/Toilet/get/', { 'filters' : json.dumps({'foo' : 666}), 'start' : 0, 'end' : 10}) 
        self.assertEqual(response.status_code, 400) 
  
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

    
