from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.dateparse import parse_datetime

from datetime import datetime
import facebook
import json
import logging
import pytz
import time
import requests

logger = logging.getLogger(__name__)

class Network(models.Model):
    """Social network (Facebook, Twitter, G+) or category of 
    identity provider (email) """
    name = models.CharField(max_length=256)

    def __str__(self):
        return 'Network {}'.format(self.name)

    class Admin(admin.ModelAdmin):
        pass

admin.site.register(Network, Network.Admin)


class Address(models.Model):
    """An Address is a vertex on a social Network. The `address` of the vertex
    is used to uniqueify it in that network.
    
    For example, a phone number is an address on the phone network.
    the 'name' of that adderss is the same as the phone number. 
    The network is 'telephone.'"""


    name = models.CharField(max_length=1024,default="")
    network = models.ForeignKey(Network)
    aliases = models.ManyToManyField('self')

    ID = 0
    USERNAME = 1
    category = models.IntegerField(default=0)

    def __str__(self):
        return '{}.{}'.format(self.network.name, self.name)


    def get_username_alias(self):
      for alias in self.aliases.filter(category=Address.USERNAME):
        return alias

      

   
    @classmethod
    def get_address_list(classs):
      result = {}
      for addr in Address.objects.all():
        result[addr.id] = addr.to_json()
      return result

    def to_json(self):
        return { 'network' : self.network.name,
                 'name' : self.name }

    class Meta:
        verbose_name_plural = 'Addresses'

    class Admin(admin.ModelAdmin):
        pass

    def get_explicit_respect(self, other_address):
      for s in self.statements_by.\
          filter(subject=other_address).\
          filter(category=Statement.get_category_by_name('RESPECT')).\
          order_by('-timestamp'):
          return s.value
      return 0

    def get_implied_respect(self, other_address):
      category = Statement.get_category_by_name('IMPLIEDRESPECT')
      for s in self.statements_by.\
        filter(
            subject=other_address,
            active=True,
            category=category).\
            order_by('-timestamp') :
        return s.value
      return 0

admin.site.register(Address, Address.Admin)

def _validate_json(body, expected):
    missing = []

    for key in expected:
        if not key in body:
            missing.append(key)
    if missing: 
        return False, { 'missing' : missing }
    else:
        return True, {}


class Statement(models.Model):
    """
        The meat of the system here. Statements can have the following category

                     
    """
    author  = models.ForeignKey(Address, related_name='statements_by')
    subject = models.ForeignKey(Address, related_name='statements_about')
    category = models.IntegerField(default=0)
    value = models.DecimalField(default=0,max_digits=6,  decimal_places=4,)
    active= models.BooleanField(default=True)

    
    # when the statement happened
    timestamp = models.DecimalField(max_digits=16,decimal_places=2)

    # where the statement happened
    source = models.CharField(default='',max_length=256)
    Categories = ['TRUST', 'TROLL', 'RESPECT', 'DISRESPECT', 'IMPLIEDRESPECT'] 
    CategoriesDict = dict([ (i, Categories[i]) for i in range(len(Categories))])

    @classmethod
    def get_category_by_name(classs, category_name):
      for i,name in zip(xrange(len(Statement.Categories)), Statement.Categories):
        if name.upper() == category_name.upper():
          return i
      raise ValueError("Category %s does not exist" % category_name)


    @property
    def category_name(self):
      return Statement.Categories[self.category]


    def __str__(self):
        return "at {}, {} says {} {}".format(self.timestamp,
                                             self.author,
                                             Statement.Categories[self.category],
                                             self.subject)

    @classmethod
    def make_implied_statement(classs,
        author_id,
        subject_id,
        value,
        timestamp = None):

      if not timestamp:
        timestamp = time.time()

      author = Address.objects.get(id=author_id)
      subject = Address.objects.get(id=subject_id)

      category = Statement.get_category_by_name('impliedrespect')

      s, created = Statement.objects.get_or_create(
          author=author,
          subject=subject,
          category=category,
          active=True,
          defaults={'timestamp' : timestamp})

      s.timestamp = timestamp
      s.value = value
      s.save()
      return s



    @classmethod
    def make_twitter_statement(classs,
        author_name,
        subject_name,
        category_name,
        value,
        url, timestamp=None):

      if not timestamp:
        timestamp = time.time()

      twitter_network, created = Network.objects.get_or_create(name='twitter')
      author, created = Address.objects.get_or_create(network=twitter_network,
                        name=author_name.lower())
      subject, created = Address.objects.get_or_create(network=twitter_network,
                        name=subject_name.lower())

      category = Statement.get_category_by_name(category_name)


      old_statements = Statement.objects.filter(
          author=author,
          subject=subject,
          category=category).\
            order_by('timestamp')


      statement, created = Statement.objects.get_or_create(author=author,
          subject=subject, category=category,
          value=value,
          source=url, defaults={'timestamp':timestamp})

      if created:
        statement.save()
        logger.info("Created new statement!")

        if old_statements.exclude(id=statement.id).count():
          old = old_statements[1]
          old.active = False
          old.save()
          logger.info('saving outdated statement %d', old.id)
      else:
        logger.info("This statement has already been created")
      return statement
admin.site.register(Statement)


class TooManyTagsException(Exception): pass
class NoTagsException(Exception): pass
class NoValidCommandPresent(Exception): pass


class FacebookPost(models.Model):
  # these correspond to facebook posts that haven't been processed  yet
  # when someone posts on the respect matrix' wall, it gets an udpate
  # it creates one of these
  # these are used to store the state of the post in case there's an error
  fbid = models.CharField(max_length=128)
  post_body = models.TextField(default='')
  reply = models.TextField(default='')
  is_post = models.BooleanField(default=False)
   

  ALL_COMMANDS = [ 'respect', 'disrespect', 'support', 'oppose', 'whois' ]

  DOC_STRING = "You need to tag exactly one person, page or cause in the post, "\
      "and you must include one of the command verbs: " + ", ".join(ALL_COMMANDS)



  def update_from_facebook(self, is_post):
      # acces token is app_id|app_secret
      graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
      this_post = graph.get_object(self.fbid)
      is_post = this_post.get('type') == 'status'
      self.is_post = is_post
      self.post_body = json.dumps(this_post)
      self.save()

      # get network
      fb_network, created = Network.objects.get_or_create(name='facebook')

      # get the author
      author_id = this_post['from']['id']

      if author_id == settings.FACEBOOK_PAGE_ID:
        # never respond to yourself
        return

      author, created = Address.objects.get_or_create(network=fb_network,
                        name=author_id)
      
      time_key = 'updated_time' if is_post else 'created_time'
      created_time = parse_datetime(this_post[time_key])
      timestamp = (created_time - datetime(1970,1,1, tzinfo=pytz.utc)).total_seconds()
      timestamp = 0 #time.time()

      command = self.get_command(this_post['message'])
      value = 0

      if (not command) and (not is_post):
        print 'not responding to non-command comments'
        return this_post


      subject = self.get_subject(this_post, command, is_post)
      if command:
        self.handle_command(
            author,
            subject,
            self.fbid,
            command,
            this_post)

            #this_post['message'])
      else:
        print 'its an invalid command', is_post
        self.respond_invalid_command()

      return this_post

  def get_command(self, message):
    commands = [ c for c in FacebookPost.ALL_COMMANDS if '#%s' % c in message]
    if len(commands) == 1:
      return commands[0]

  def get_response_fbid(self):
    if self.is_post:
      return self.fbid
    # if it's a comment, see if it's a root comment
    graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
    this_post = graph.get_object(self.fbid,fields='can_comment')
    if this_post['can_comment']:
      return self.fbid
    this_post = graph.get_object(self.fbid,fields='parent')
    return this_post['parent']['id']

  def get_cause_subject(self, post):
    message = post['message']

    hash_words = [ word for word in message.split(' ') if \
        (word and word[0] == '#')]
    print hash_words

    if len(hash_words) > 1:
      cause = hash_words[1] 
      network, created =  Network.objects.get_or_create(name='__causes__')
      subject, created = Address.objects.get_or_create(
        network=network,
        name=cause)
      return subject
    tags = post.get('message_tags') or []
    is_post = post.get('type') == 'status'
    if tags and is_post:
      # post tags show up weird
      tags = self.convert_post_tags_to_sane_format(tags)

    if len(tags) == 0:
      self.respond_no_tags()
      return 
    elif len(tags) > 1:
      self.respond_too_many_tags()
      return

    for tag in tags:
      subject_id = tag['id']
      break

    fb_network, created = Network.objects.get_or_create(name='facebook')
    subject, created = Address.objects.get_or_create(network=fb_network,
                        name=subject_id)

    return subject


  def convert_post_tags_to_sane_format(self, post_tags):
    return [ l[0] for l in  post_tags.values() ]

  def get_subject(self, post, command, is_post):
    tags = post.get('message_tags') or []
    is_post = post.get('type') == 'status'
    if tags and is_post:
      # post tags show up weird
      tags = self.convert_post_tags_to_sane_format(tags)

    if command in ['support', 'oppose', 'whois'] :
      return self.get_cause_subject(post)
    if len(tags) == 0:
      self.respond_no_tags()
      return 
    elif len(tags) > 1:
      self.respond_too_many_tags()
      return

    subject_id = None

    for tag in tags:
      subject_id = tag['id']
      break
   

    fb_network, created = Network.objects.get_or_create(name='facebook')
    subject, created = Address.objects.get_or_create(network=fb_network,
                        name=subject_id)

    return subject

  def get_subject_name(self, post):
    tags = post.get('message_tags') or []
    is_post = post.get('type') == 'status'
    if tags and is_post:
      tags = self.convert_post_tags_to_sane_format(tags)
    if len(tags) == 0:
      return  None

    subject_name = None
    for tag in tags:
      return tag['name']
    return None

  def handle_command(self, author, subject, source, command, post):
    getattr(self, 'handle_%s' % command)(author, subject, source, post)
      
  def handle_whois(self, author, subject, source, post):
    explicit = author.get_explicit_respect(subject)
    implied = author.get_implied_respect(subject)
    message = "Explicit respect: %0.3f. Implied respect: %0.3f"
    message = message % (explicit, implied)
    self.respond_to_post(message)

  
  def handle_respect(self, author, subject, source, post):
    return self._handle_respect(author, subject, 1, source, post)

  def handle_disrespect(self, author, subject, source, post):
    return self._handle_respect(author, subject, -1, source, post)

  def _handle_respect(self, author, subject, value, source, post):
      category=Statement.get_category_by_name('RESPECT')
      s, created = Statement.objects.get_or_create(
        author=author,
        subject=subject,
        value=value,
        category=category,
        source=self.fbid,
        defaults={'timestamp':time.time()})
      self.respond_success(subject, category, value, post)
      return s

  def handle_support(self, author, cause, source, post):
    self._handle_respect(author, cause, 1, source, post)

  def handle_oppose(self, author, cause, source, post):
    self._handle_respect(author, cause, -1, source, post)


  def respond_no_tags(self):
    message = "Sorry, that is not a valid request; nobody is tagged and no cause is specified. "+\
        FacebookPost.DOC_STRING
    self.respond_to_post(message)

  def respond_too_many_tags(self):
    message = "Sorry, that is not a valid request; "+\
       "too many people are tagged. " + FacebookPost.DOC_STRING
    self.respond_to_post(message)

  def respond_invalid_command(self):
    message = "Sorry, that is not a valid request. "+FacebookPost.DOC_STRING
    self.respond_to_post(message)

  def get_action_text(self, subject, value):
    if subject.network.name == "__causes__" : 
      if value == 1:
        return 'support'
      else:
        return 'oppose'
    else:
      if value == 1:
        return 'respect'
      else:
        return 'disrespect'

  def respond_success(self, subject, category, value, post):
    if subject.network.name == '__causes__':
      subject_name = subject.name
    else:
      subject_name = self.get_subject_name(post)
    action = self.get_action_text(subject, value)
    message = "Recorded that you %s %s." % (action, subject_name)
    self.respond_to_post(message)

  def respond_to_post(self, message):
    graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
    response_fbid = self.get_response_fbid()
    graph.put_object(response_fbid, 'comments', message=message)


  class Admin(admin.ModelAdmin):
   pass

admin.site.register(FacebookPost)

 



