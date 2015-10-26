from drops.models import Statement
from drops.models import Address
from django.db.models import Max

import scipy.sparse
import time

  

def make_empty_matrix():
  total_addresses = Address.objects.count()
  size = total_addresses + 1
  M = scipy.sparse.lil_matrix((size,size),
      dtype='float32')

  return M


def make_matrix(is_positive=True):
  timestamp =  time.time()

  # addresses ids count from 1
  # to make everyone happy, there'll be a 0 entry who says nothing

  M = make_empty_matrix()
  size = M.get_shape()[0]

  respect_category = Statement.get_category_by_name('RESPECT')
  filters =  { 'active' : True,
              'timestamp__lte' : timestamp,
              'category' : respect_category,
              'author__id__lt' : size,
              'subject__id__lt' : size}

  if is_positive:
    filters['value__gt'] = 0.0
  else:
    filters['value__lt'] = 0.0

  for s in Statement.objects.\
      filter(**filters).\
      order_by('subject'):
      M[s.author.id, s.subject.id] = s.value

  return M


def make_implied_matrix(levels=3,decay=0.5):
  positives = make_matrix()
  negatives = make_matrix(False)
  p_cs = (decay*positives)
  n_cs = (decay*negatives)
  result = positives + negatives
  p_product = positives
  print result.toarray().tolist()
  for i in xrange(1,levels):
    n_product = p_product*n_cs
    p_product =  p_product*p_cs
    result = result + n_product + p_product
    print result.toarray().tolist()
  return result

