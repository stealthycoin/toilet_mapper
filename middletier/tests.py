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
        self.assertEqual(response.content, "Toilet does not exist")

    def test_missing_attributes(self):
        request = self.factory.post('/query/put/', {'table' : 'review'});
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Missing Attributes")

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
        self.assertEqual(response.content, "Review does not exist")

    def test_edit_no_pk(self):
        request = request = self.factory.post('/query/put/',
                                  {'table' : 'review', 
                                    'update' : 'True',
                                    'content': "Foo bar"})
        request.user = self.user
        response = put(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, "Missing Attributes")
         

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
 
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

