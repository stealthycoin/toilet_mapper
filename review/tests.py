"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from toilet.middletier import listing
from django.test.client import Client
from django.contrib.auth.models import User
from review.models import Review
from toilet.models import Toilet
import json
import datetime
import unittest


from django.test import TestCase
class putNewReviewTest(TestCase):
    def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
      self.user.save()
      self.toilet = Toilet(date = datetime.datetime.now() ,
                            creator = self.user, name = "test_toilet")
      self.toilet.save()
    
    def test_put_new_review(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 5, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 201)
      review = Review.objects.get(content='This is a dumb test')
      responcedict = json.loads(response.content)
      self.assertEqual(review.id, responcedict[0]['pk'])
   
    def test_put_no_toilet(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      response = self.client.post('/api/review/create/', {'toilet' : 666, 'rank' : 5, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 404)
    @unittest.skip("Not sure what we should do in this case")
    def test_missing_attributes(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')

    def test_post_review_twice(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 5, 'content' : 'This is a dumb test'})
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 5, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 403)

class GetReviewTest(TestCase):
    def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
      self.user.save()
      self.user_two = User.objects.create_user('test_bar', 'foo@bar.com', 'bqz_qux')
      self.user_two.save()
      self.toilet = Toilet(date = datetime.datetime.now() ,
                            creator = self.user, name = "test_toilet")
      self.toilet.save()
      self.toilet_second = Toilet(date = datetime.datetime.now(),
                           creator = self.user, name = "test_toilet2")
      self.toilet_second.save()
      self.review_one_one = Review(user=self.user, date = datetime.datetime.now(),
                               toilet = self.toilet, content = "foo bar", rank = 5,
                               up_down_rank = 1)
      self.review_one_one.save() 
      self.review_one_two = Review(user=self.user, date = datetime.datetime.now(),
                               toilet = self.toilet_second, content = "foo bar", rank = 5,
                               up_down_rank = 1)
      self.review_one_two.save()
      self.review_two_one =  Review(user=self.user_two, date = datetime.datetime.now(),
                               toilet = self.toilet, content = "foo bar", rank = 5,
                               up_down_rank = 1)
      self.review_two_one.save()
      self.review_two_two =  Review(user=self.user_two, date = datetime.datetime.now(),
                               toilet = self.toilet_second, content = "foo bar", rank = 5,
                               up_down_rank = 1)
      self.review_two_two.save()
    
    def test_get_review_user(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'user' : self.user.id}) })
      responselist = json.loads(response.content)
      #there are two reviews per user
      self.assertEqual(len(responselist), 2)
      for review in responselist:
          self.assertEqual(review['fields']['user'], self.user.id)

    def test_get_review_by_toilet(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'toilet' : self.toilet.id})})
      responselist = json.loads(response.content)
      #there are two reviews per toilet
      self.assertEqual(len(responselist), 2)
      for review in responselist:
          self.assertEqual(review['fields']['toilet'], self.toilet.id)

    def test_get_review_by_non_exist_toilet(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'toilet' : 666})})
      #not sure if we should return 404 or not
      self.assertEqual(json.loads(response.content), [])
   
    def test_get_review_by_not_existant_user(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'user' : 666}) }) 
      #not sure if we should return 404 or not
      self.assertEqual(json.loads(response.content), [])


 
      

      


     

    

