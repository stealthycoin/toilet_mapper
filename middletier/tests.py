"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase, RequestFactory
from toilet.models import Toilet
from review.models import Review
from django.contrib.auth.models import User
from middletier.views import put, get, remove_json_characters 
from django.http import HttpResponse, HttpRequest
import json
import datetime
import re


class putNewReview(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()
        self.toilet = Toilet(date = datetime.datetime.now() ,
                            creator = self.user, name = "test_toilet")
        self.toilet.save()
        
    def test_put_new_review(self):
        request = postReview(self.factory, self.toilet.pk, "foo bar baz qux")
        request.user = self.user
        response = put(request)
        #201 for new resource created
        self.assertEqual(response.status_code, 201)
        review = Review.objects.get(content="foo bar baz qux")
        responseId = getPkFromResponse(response)
        self.assertEqual(responseId, review.pk)

    def test_put_no_toilet(self):
        request = postReview(self.factory, 123, "foo bar baz qux");
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, "Toilet matching query does not exist.")

    def test_missing_attributes(self):
        request = self.factory.post('/query/put/', {'table' : 'review'});
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Missing toilet attribute")

    def test_edit_review(self):
        request = postReview(self.factory, 1, "Old Connent")
        request.user = self.user
        response = put(request) 
        responsePK = getPkFromResponse(response)
        request = postReview(self.factory, 1, "New Content", update=True,reviewPK=responsePK)
        request.user = self.user
        response = put(request)
        review = Review.objects.get(pk=responsePK)
        self.assertEqual(review.content ,"New Content")

    def test_edit_no_review(self):
        request = postReview(self.factory, 666, "New Content", update=True, reviewPK = 666)
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, "Review matching query does not exist.")

    def test_edit_no_pk(self):
        request = self.factory.post('/query/put/',
                                  {'table' : 'review', 
                                    'update' : 'True',
                                    'content': "Foo bar"})
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Missing pk attribute")

    def test_edit_no_content_or_rank(self):  
        request = postReview(self.factory, 1, "Old Connent")
        request.user = self.user
        response = put(request) 
        responsePK = getPkFromResponse(response)
        request = self.factory.post('/query/put/',
                                  {'table' : 'review', 
                                    'update' : 'True',
                                    'pk': responsePK})
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Missing more than one attribute")

    def test_post_wrong_type_pk(self):
        request = postReview(self.factory, "not a number", "Old Connent")
        request.user = self.user
        response = put(request) 
        self.assertEqual(response.status_code, 400)
  
    def test_post_wrong_type_content(self):
        request = postReview(self.factory, 1, 666)
        request.user = self.user
        response = put(request) 
        self.assertEqual(response.status_code, 201)
   
    def test_post_review_twice(self):
        request = postToilet(self.factory, "Toilet 1") 
        request.user = self.user
        response = put(request)
        toilet_pk = json.loads(response.content)[0]['pk']
        request = postReview(self.factory, toilet_pk, "First Review") 
        request.user = self.user
        response = put(request)
        request = postReview(self.factory, toilet_pk, "Review Again")
        request.user = self.user
        response = put(request)
        #can't submit multiple reviews
        self.assertEqual(response.status_code, 415, "Database allows posting more than one review to the same toilet") 

class testPutToilet(TestCase):
    def setUp(self):
       self.factory = RequestFactory()
       self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
       self.user.save()
    
    def test_post_toielt(self):
       request = postToilet(self.factory, "Test Toilet")
       request.user = self.user
       response = put(request)
       toiletPK = getPkFromResponse(response)
       toilet = Toilet.objects.get(name="Test Toilet")
       self.assertEqual(toiletPK,toilet.pk)

    def test_no_table(self): 
       request = self.factory.post('/query/put', {'pk' : 1})
       request.user = self.user
       response = put(request)
       self.assertEqual(response.status_code, 400)
 

class getReview(TestCase):
    def setUp(self):
      self.factory = RequestFactory()
      self.user = User.objects.create_user("test_foo", "foo@bar.com", "password")
      self.user.save()
      
    def test_get_review_by_toilet(self):
      toilet = Toilet()
      toilet.name = "New Toilet"
      toilet.date = datetime.datetime.now()
      toilet.creator = self.user 
      toilet.save()
      review = Review()
      review.toilet = toilet
      review.content = "This is a test review"
      review.rank = 0
      review.user = self.user
      review.date = datetime.datetime.now()
      review.save()
      request = getReviewByToilet(self.factory, toilet.pk)
      request.user = self.user
      response = get(request)
      response_list = json.loads(response.content)
      self.assertEqual(response_list[0]['pk'], review.pk)
   
    def test_get_review_by_user(self):
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
      review = Review()
      review.toilet = toilet
      review.content = "First toilet content"
      review.rank = 0
      review.user = self.user
      review.date = toilet.date
      review.save()
      second_review = Review()
      second_review.toilet = second_toilet
      second_review.user = self.user
      second_review.date = second_toilet.date
      second_review.rank = 0
      second_review.content = "Second toilet content"
      second_review.save()
      request = getReviewByUser(self.factory, self.user.pk)
      response = get(request)
      response_list = json.loads(response.content)
      pk_list = [pk_elm for pk_elm in [ elm_list['pk']
                                      for elm_list in response_list]]
      self.assertEqual(len(pk_list), 2)
      self.assertIn(review.pk, pk_list)
      self.assertIn(second_review.pk, pk_list)

    def test_get_review_no_table(self):
      request = self.factory.get('query/get/')
      request.user = self.user  
      response = get(request)
      self.assertEqual(response.status_code, 400)

    #doesnt do anything at the moment 
    def test_get_review_no_query(self):
      request = self.factory.get('query/get/?table=review') 
      request.user = self.user
      response = get(request)
      #this test is just here, we should discuss what do when this happens
      #self.assertEqual(response.status_code, 400)
    
    def test_get_bad_table(self):
      request = self.factory.get('query/get/?table=foo') 
      request.user = self.user
      response = get(request)
      self.assertEqual(response.status_code, 400)

class getToilet(TestCase):
    def setUp(self):
      self.factory = RequestFactory()
      self.user = User.objects.create_user("test_foo", "foo@bar.com", "password")
      self.user.save()
    
    def get_toilet_by_id(self):
      toilet = Toilet()
      toilet.name = "New toilet"
      toilet.date = datetime.datetime.now()
      toilet.creator = self.user
      toilet.save()
      request = getToiletById(self.factory, toilet.pk)
      request.user = self.user
      response = get(request)
      toilet_pk = json.loads(response.content)[0]['pk']
      self.assertEqual(toilet_pk, toilet.pk)
    
    def get_toilet_by_user(self):
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
      request = getToiletByUser(self.factory, self.user.pk)
      request.user = self.user
      response = get(request)
      response_list = json.loads(response.content)
      pk_list = [pk_elm for pk_elm in [ elm_list['pk']
                                      for elm_list in response_list]]
      self.assertEqual(len(pk_list), 2)
      self.assertIn(toilet.pk, pk_list)
      self.assertIn(second_toilet.pk, pk_list)



def getToiletById(factory, toilet):
    return factory.get('/query/get/?table=toilet&pk=' + str(toilet) )

def getToiletByUser(factory, user):
    return factory.get('/query/get/?table=toilet&user=' + str(user) )

def getReviewByToilet(factory,toilet):
    return factory.get('/query/get/?table=review&toilet=' + str(toilet) )

def getReviewByUser(factory, user):
    return factory.get('/query/get/?table=review&user=' + str(user) )

def getPkFromResponse(response):
    return int(re.search(r'\"pk\": (\d+)', response.content).group(1))

def postReview(factory, toilet, content, update=False, reviewPK=0):
    request = 0
    if(update == True):
        request = factory.post('/query/put/',
                                  {'table' : 'review', 
                                    'pk' : reviewPK,
                                    'update' : 'True',
                                    'content': content})
    else:
       request = factory.post('/query/put/',
                                  {'table' : 'review', 
                                    'toilet' : toilet,
                                    'content': content})
    return request

def postToilet(factory,name, update=False, pk=0):
   request = 0
   if update:
      x = 1
      #nothing yet 
   else :
      request = factory.post('/query/put/',
                              {'table' : 'toilet',
                                'name' : name})
   return request

