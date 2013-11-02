"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from toilet.middletier import listing
from django.test.client import Client

class ToiletTest(TestCase):
    
    def setUp(self):
        print "Setting up toilet tests"
        c = Client()
        self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
        self.user.save()
    
    def get_toilet_no_login(self):
        print "Wtf mate"
        c.user= self.user
        response = c.post('/api/add/toilet', {'data' : 'djdjdjkekle' })
        print response


