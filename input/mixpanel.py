import requests
import time
import json
import hashlib
import urllib

from datetime import datetime
from adapter.utils import Logger
from input.models import Record
logger = Logger()

API_KEY = 'fcc50d5150c1b242626ea3d3515ad4d7'
API_SECRET = '20ba853fc59a22d82eefc741279fa378'
ENDPOINT = 'http://mixpanel.com/api'
VERSION = '2.0'
TODAY = datetime.today()
A_WEEK = 7
A_DAY = 1
A_WEEK_AGO = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 7)
YESTERDAY = '%s-%s-%s' % (TODAY.year, TODAY.month, TODAY.day - 1)
EXPIRE = int(time.time()) + 600


class Scraper(object):

    def __init__(self):
        # TODO:
        #   setup a method for getting yesterdays dau
        #   setup a method for getting yesterdays revenue
        #   save as a new record
        self.get_dau()
        super(Scraper, self).__init__()

    def unicode_urlencode(self, params):
        """ Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

    def hash_args(self, args, secret=None):
        """ Hashes arguments by joining key=value pairs, appending a secret, and
            then taking the MD5 hex digest.
        """
        for a in args:
            if isinstance(args[a], list):
                args[a] = json.dumps(args[a])

        args_joined = ''
        for a in sorted(args.keys()):
            if isinstance(a, unicode):
                args_joined += a.encode('utf-8')
            else:
                args_joined += str(a)

            args_joined += '='

            if isinstance(args[a], unicode):
                args_joined += args[a].encode('utf-8')
            else:
                args_joined += str(args[a])

        hash = hashlib.md5(args_joined)

        if secret:
            hash.update(secret)
        elif API_SECRET:
            hash.update(API_SECRET)
        return hash.hexdigest()

    def get_dau(self):
        DAU_EVENT = 'Loaded Game'
        params = {
            'api_key': API_KEY,
            'expire': EXPIRE,
            'interval': A_DAY,
            'type': 'unique',
            'unit': 'day',
            'event': [DAU_EVENT]
        }
        params['sig'] = self.hash_args(params)
        url = '/'.join([ENDPOINT, str(VERSION)]) + '/events/?' + self.unicode_urlencode(params)
        logger.debug('url: %s' % url)
        r = requests.get(url)
        logger.debug('YESTERDAY: %s' % YESTERDAY)
        dau = r.json()['data']['values'][DAU_EVENT][YESTERDAY]
        record, created = Record.objects.get_or_create(date=YESTERDAY)
        record.dau = dau
        record.save()
        logger.debug('created: %s' % created)
        logger.debug('record: %s' % record)

    def save_as_record(self, data):
        logger.debug('data:')
        logger.debug(data)
        # Go through each item
        # Store in dict with keys by date
        # then go through each day of the dict
        # calculate the data points we want
        # save it as a record
        # then go back to testing the export
