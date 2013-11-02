"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from toilet.middletier import listing
from django.test.client import Client
from django.contrib.auth.models import User

class ToiletTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()
 
    def test_get_toilet_not_logged_in(self):
        self.client.user = None
        response = self.client.post('/api/toilet/create/', {'data' : 'djdjdjkekle' })
        self.assertEqual(response.status_code, 401)
        print response

    def test_get_toilet_logged_in_bad_data(self):
        self.client.user = self.user
        print self.user.username
        print self.user.password
        self.client.post('/api/user/login/', {'username' : 'test_foo'
                                              ,'password': 'bqz_qux'})
        response = self.client.post('/api/toilet/create/', {'data' : 'djdjdjkekle' })
        self.assertEqual(response.status_code, 400)
        print response
