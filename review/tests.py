"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from review.models import Review, Vote
from toilet.models import Toilet
import json
import datetime
import unittest
import random

"""
Add Review Equivalence Classes (Ace):
- EQ 1: Restroom Exists, User Logged in, Len >= 5, 1 <= Rank <=5, New Review
- EQ 2: Restroom Does Not Exist, User Logged in, len >= 5, 1 <= Rank <=5, New Review
- EQ 3: Restroom Exists, User not logged in, len >= 5, 1 <= Rank <= 5, New Review
- EQ 4: Restroom Exists, User Logged in, Len < 5, 1 <= Rank <= 5, New Review
- EQ 5: Restroom Exists, user Logged in, Len >= 5, Rank >5 or Rank < 1, New Review
- EQ 6: Restroom Exists, User Logged in, len >= 5, 1 <= Rank <= 5, User has already created review

Retrieve Review Equivalence Classes (Ace):
- EQ 1: Restroom exists
- EQ 2: Restroom does not exist
- EQ 3: User exists
- EQ 4: User does not exists

Up/Down Vote Reviews Equivalence Classes (Jeremey):
  -EQ 1: review_pk = existing review, Number of times voting = 1, user logged in
  -EQ 2: review_pk = non existing review, Number of times voting = 1, user logged in
  -EQ 3: review_pk = existing review, Number of times voting = 2, user logged in
  -EQ 4: review_pk = existing review, Number of times voting = 1, user not logged in
 +

"""


from django.test import TestCase
class putNewReviewTest(TestCase):
    def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
      self.user.save()
      self.toilet = Toilet(date = datetime.datetime.now() ,
                            creator = self.user, name = "test_toilet")
      self.toilet.save()
    #Add a new review with rank 3 to test toilet, EQ1 
    def test_put_new_review(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 3, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 201)
      review = Review.objects.get(content='This is a dumb test')
      responcedict = json.loads(response.content)
      self.assertEqual(review.id, responcedict[0]['pk'])
      #make sure that the rating updated
      self.assertEqual(Toilet.objects.get(pk=self.toilet.id).rating, 3)
      
   #add review to a toilet that does not exists, EQ2
    def test_put_no_toilet(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      response = self.client.post('/api/review/create/', {'toilet' : 666, 'rank' : 5, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 400)

    #add review not logged in, EQ3
    def test_put_not_logged_in(self):
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.pk, 'rank' : 5, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 403) 

    #add review content is to short, EQ4
    def test_put_to_short(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 3, 'content' : ''})
      self.assertEqual(response.status_code, 400)

    # add review rank is invalid, EQ5
    def test_put_invalid_rank(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 7, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 400)
      
    #Try to post a review twice on the same toilet, EQ6
    def test_post_review_twice(self):
      self.client.login(username=self.user.username, password = 'bqz_qux')
      self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 5, 'content' : 'This is a dumb test'})
      response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : 5, 'content' : 'This is a dumb test'})
      self.assertEqual(response.status_code, 403)

    #post many reviews on the same toilet (from different users)
    def test_post_review_many(self): 
      rating_sum = 0
      #generate randomw ratings for the reviews
      ratings = [random.randint(1,5) for x in xrange(10)] 
      #for each rating, create user and add the review check for the right average on toilet ratings
      for counter, rating in enumerate(ratings):
         rating_sum += rating
         username = 'test_bar' + str(counter)
         ratingUser = User.objects.create_user(username, username + '@bar.com', 'password')
         ratingUser.save()
         self.client.login(username=username,password ='password')
         response = self.client.post('/api/review/create/', {'toilet' : self.toilet.id , 'rank' : rating, 'content' : 'This is a dumb test with rating' + str(rating)})
         avg = float(rating_sum)/ (counter + 1)
         toilet = Toilet.objects.get(pk=self.toilet.pk)
         self.assertEqual(round(float(toilet.rating), 6), round(avg, 6))

class UpDownVoteTest(TestCase):
    def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user('test_foo', 'foo@bar.com','bqz_qux')
      self.user.save()
      self.user_two = User.objects.create_user('test_bar', 'foo@bar.com', 'bqz_qux')
      self.user_two.save()

      self.toilet = Toilet(date = datetime.datetime.now() ,
                            creator = self.user, name = "test_toilet")
      self.toilet.save()
      self.review_one_one = Review(user=self.user, date = datetime.datetime.now(),
                               toilet = self.toilet, content = "foo bar", rank = 5,
                               up_down_rank = 0)
      self.review_one_one.save() 
      self.review_two_one =  Review(user=self.user_two, date = datetime.datetime.now(),
                               toilet = self.toilet, content = "foo bar", rank = 5,
                               up_down_rank = 0)
      self.review_two_one.save()
      
    #Upvote review 
    def test_up_vote_review(self):
      self.client.login(username=self.user.username, password='bqz_qux')
      response = json.loads(self.client.post('/api/review/upvote/', {'review_pk': self.review_one_one.pk}).content)[0]
      updatedreview = Review.objects.get(pk=self.review_one_one.pk)
      self.assertEqual(updatedreview.up_down_rank, 1)
    
    #Try to upvote a review twice, only add the upvote once
    def test_up_vote_twice(self):
      vote = Vote(review=self.review_one_one, user = self.user_two, vote = 1) 
      vote.save()
      self.review_one_one.up_down_rank += 1
      self.review_one_one.save()
      self.client.login(username=self.user_two.username, password='bqz_qux')
      response = json.loads(self.client.post('/api/review/upvote/', {'review_pk': self.review_one_one.pk}).content)[0]
      self.assertEqual(response['fields']['up_down_rank'],1)

    #Try to upvote when not logged in
    def test_up_vote_not_logged_in(self):
      response = self.client.post('/api/review/upvote/', {'review_pk': self.review_one_one.pk})
      self.assertEqual(response.status_code, 403)

    #upvote without review information
    def test_up_vote_no_data(self):
      self.client.login(username=self.user_two.username, password='bqz_qux')
      response = self.client.post('/api/review/upvote/' )
      self.assertEqual(response.status_code, 400)

    def test_up_vote_get(self):
      self.client.login(username=self.user_two.username, password='bqz_qux')
      response = self.client.get('/api/review/upvote/' )
      self.assertEqual(response.status_code, 415)
    #upvote a review that doesn't exist
    def test_up_vote_no_review(self):
      self.client.login(username=self.user_two.username, password='bqz_qux')
      response = self.client.post('/api/review/upvote/', {'review_pk': 666})
      self.assertEqual(response.status_code, 400)
    #downvote a review
    def test_down_vote(self):
      self.client.login(username=self.user_two.username, password='bqz_qux')
      response = json.loads(self.client.post('/api/review/downvote/', {'review_pk' : self.review_one_one.pk}).content)[0]
      self.assertEqual(response['fields']['up_down_rank'], -1)
      
    #Test down vote and upvote on same review 
    def test_down_after_up_vote(self):
      vote = Vote(review=self.review_one_one, user = self.user_two, vote = 1) 
      vote.save()
      self.review_one_one.up_down_rank += 1
      self.review_one_one.save()
      self.client.login(username=self.user_two.username, password='bqz_qux')
      response = json.loads(self.client.post('/api/review/downvote/', {'review_pk': self.review_one_one.pk}).content)[0]
      self.assertEqual(response['fields']['up_down_rank'],0)

      
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
      
    #get all reviews by user EQ3
    def test_get_review_user(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'user' : self.user.id}) })
      responselist = json.loads(response.content)
      #there are two reviews per user
      self.assertEqual(len(responselist), 2)
      for review in responselist:
          self.assertEqual(review['fields']['user'], self.user.id)
          
    #get all reviews by toilet id EQ1
    def test_get_review_by_toilet(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'toilet' : self.toilet.id})})
      responselist = json.loads(response.content)
      #there are two reviews per toilet
      self.assertEqual(len(responselist), 2)
      for review in responselist:
          self.assertEqual(review['fields']['toilet'], self.toilet.id)
          
    #get all reviews by a toilet that does not exist EQ2
    def test_get_review_by_non_exist_toilet(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'toilet' : 666})})
      self.assertEqual(json.loads(response.content), [])
      
    #get all reviews by user tht doesn't exists EQ4
    def test_get_review_by_not_existant_user(self):
      response = self.client.post('/api/Review/get/', { 'start' : 0, 'end' : 10, 'filters' : json.dumps({'user' : 666}) }) 
      self.assertEqual(json.loads(response.content), [])


 
      

      


     

    

