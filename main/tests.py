"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

"""

Create user equiv classes
 -EQ 1: Name is unique
 -EQ 2: Name is already taken


Reporting equiv classes
 -EQ 1: Reporting someone increments their spam counter

"""

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
