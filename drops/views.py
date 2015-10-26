from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from drops.models import Address
from drops.models import Network
from drops.models import Statement
from drops.models import FacebookPost
from drops.models import TooManyTagsException
from drops.models import NoTagsException
from drops.models import NoValidCommandPresent
from drops.models import _validate_json

import json
import logging
import time

logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse(':)')


def _make_statement(request):

    # first get the body to make sure this guy is valid
    body = json.loads(request.body)

    expected = [ 'category' ]

    valid, errors = _validate_json(body, expected)
    if not valid:
        return JsonResponse({'success' : False,
                                'errors' : errors })
                                            
    # extract the fields from the body 
    # create the appropriate networks/addresses if needed

    category = body['category']
    subj_network_name = body['author_network']
    auth_name = body['author_name']
    
    s_network, created = Network.objects.get_or_create(name=subj_network_name)
    if created: s_network.save()

    subject, created = Address.objects.get_or_create(name=subj_name,
                                                     network=s_network)
    if created: subject.save()

    s = Statement.create(author, content, subject)
    s.save()

    return JsonResponse({'success' : True,
                           'id' : s.id})

@csrf_exempt
def facebook_post(request):
  print "--request is ---\n%s\n----" % request.body
  
  post_data = None
  try:
    post_data = json.loads(request.body)
    for entry in post_data['entry']:
      for change in entry['changes']:
        if change['field']  == 'feed' and\
           not (change['value']['verb'] == 'remove'):
          post_id = None
          created = None
          post = None
          if change['value']['item'] == 'post' :
            post_id = change['value']['post_id']
            is_post = True
            print 'its a post'
          elif change['value']['item'] == 'comment':
            post_id = change['value']['comment_id']
            is_post = False
            print 'its a comment'
          if post_id:
            post, created = FacebookPost.objects.get_or_create(fbid=post_id)
          else:
            print 'got some weird value here', change['value']['item']
          if created:
            print 'made a new post'
          else:
            print 'an existing post could be used'
          try:
            if post:
              post.update_from_facebook(is_post)
          except NoTagsException as e:
            print ('no such tags!')


  except ValueError as ve:
    print 'had value error', ve
  except KeyError as ke:
    print ('had key error: ', ke)

  # check for new subscription
  challenge = request.GET.get('hub.challenge','')
  return HttpResponse(challenge)
  

def check_statement(request,
                    author_network, author_name,
                    content,
                    subject_network, subject_name):


    for s in Statement.objects.filter(author__network__name=author_network,
                                author__name=author_name,
                                content=content,
                                subject__network__name=subject_network,
                                subject__name=subject_name).\
                                order_by('-timestamp'):
        return JsonResponse({ 'exists' : True,
                                'timestamp'  : s.timestamp})
    return JsonResponse({ 'exists' : False })


def stating_addresses(request, content, subject_network, subject_name):
    by_network = {}
    last_maker = None
    for s in Statement.objects.filter(subject__network__name=subject_network,
                                      subject__name=subject_name,
                                      content=content).\
                                      order_by('timestamp', 'author'):
        if last_maker is None or (s.author.id != last_maker.id):
            auth_network = s.author.network.name
            auth_name = s.author.name
            authors = by_network.setdefault(auth_network,[])
            authors.append([s.timestamp,auth_name])
        last_maker = s.author

    return JsonResponse({'authors' : by_network})
            



