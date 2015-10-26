from django.test import TestCase
import functools
import re

from drops.models import FacebookPost

def use_fbid(fbid):
  def wrapper(f):
    @functools.wraps(f)
    def real_wrapper(*args, **kwargs):
      p = FacebookPost(fbid=fbid)
      p.update_from_facebook(True)
      return f(*args,**kwargs)
    return real_wrapper
  return wrapper



class SamplePostsRegexTest(TestCase):

  def setUp(self):
    self.message = None
    self.response_fbid = None
    def mock_respond(mock_self, message):
      print 'got message', message

      self.message = message
      self.response_fbid = mock_self.get_response_fbid()
    FacebookPost.respond_to_post =  mock_respond


  def assertResponseMatchesRegex(self, r):
    regex = re.compile(r)
    self.assertTrue(regex.search(self.message))

 
  @use_fbid("889318221134496_927729230626728")
  def test_opposeCause(self):
    self.assertResponseMatchesRegex("oppose")
    self.assertResponseMatchesRegex("#IStandWithAhmed")

  @use_fbid("889318221134496_927728710626780")
  def test_respectPerson(self):
    self.assertResponseMatchesRegex("respect")
    self.assertResponseMatchesRegex("Matt Steinberg")

  @use_fbid("889318221134496_927698573963127")
  def test_whoisPerson(self):
    self.assertResponseMatchesRegex("Explicit respect")
    self.assertResponseMatchesRegex("Implied respect")

  @use_fbid("889318221134496_927200750679576")
  def test_selfPost(self):
    self.assertIsNone(self.message)

  @use_fbid("930638203669164_930640460335605")
  def test_selfPost(self):
    self.assertResponseMatchesRegex("respect")
    self.assertResponseMatchesRegex("Mark P Xu Neyer")


  @use_fbid("930638203669164_930647827001535")
  def test_commentWithNewlines(self):
    self.assertResponseMatchesRegex("Explicit respect")
    self.assertResponseMatchesRegex("Implied respect")

