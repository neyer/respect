from django.core.management.base import BaseCommand
import itertools
import logging
import requests
from drops.models import Statement

logging.basicConfig()
logger = logging.getLogger(__name__)

LOOP_PERIOD = 30

BLOCKLIST_URL = "http://www.theblockbot.com/sign_up/followthefollowers/blocks.csv"


def by_two(iterable):
    "Collect data into length2 chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * 2
    return itertools.izip_longest(fillvalue=None, *args)

class Command(BaseCommand):

  def handle(self, *args, **options):
    logger.info("Downloading blocklist")
    r = requests.get(BLOCKLIST_URL)

    logger.info("Got blocklist")

    parts = r.content.split(",")
    for name, block_level in by_two(parts):
      logger.info("%s blocked at level %s", name, block_level)
