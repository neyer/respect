from django.core.management.base import BaseCommand, CommandError
from drops import matrix
from drops.models import Address
from drops.models import Statement
from optparse import make_option
import logging
import json
import time

logging.basicConfig()
logger = logging.getLogger(__name__)


class Command(BaseCommand):

  option_list = BaseCommand.option_list + (
      make_option('--loop',
        default=False,
        dest='loop',
        action='store_true'),
       make_option('--sleep-time',
          default=60,
          dest='sleep_time',
          ),
    )

  def handle(self, *args, **options):

    while options.get('loop'):
      logger.info("##### constructing matrix");
      self.make_it()
      logger.info("##### sleeping a bit");
      time.sleep(float(options.get('sleep_time')) or 60)

  def make_it(self):
    explicit_p = matrix.make_matrix() 
    explicit_n = matrix.make_matrix(False) 

    explicit = explicit_p + explicit_n

    res = {}
    res['explicit' ] = explicit.toarray().tolist()

    implied = matrix.make_implied_matrix(levels=4)

    print 'implied is', implied.toarray().tolist()

    size, _ = implied.get_shape()

    implied_list =  implied.toarray().tolist()

    for source, row in zip(xrange(size), implied_list):
      for dest, value in zip(xrange(size), row):
        if value:
          print 'adding satement by %d about %d' % (source, dest)
          Statement.make_implied_statement(source, dest, value)

