import requests
import time
import json
import hashlib
import urllib
import datetime

from adapter.utils import Logger
from input.models import Record
logger = Logger()

API_KEY = 'fcc50d5150c1b242626ea3d3515ad4d7'
API_SECRET = '20ba853fc59a22d82eefc741279fa378'
ENDPOINT = 'http://mixpanel.com/api'
VERSION = '2.0'
A_DAY = 1
TODAY = datetime.datetime.today()
YESTERDAY = (TODAY - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
TWO_DAYS_AGO = (TODAY - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
THREE_DAYS_AGO = (TODAY - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
WEEK_AGO = (TODAY - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
MONTH_AGO = (TODAY - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
EXPIRE = int(time.time()) + 600


class Scraper(object):

    def __init__(self):
        record, created = Record.objects.get_or_create(date=YESTERDAY)
        logger.debug('created: %s' % created)
        logger.debug('record: %s' % record)
        record.dau = self.get_dau()
        record.revenue = self.get_revenue()
        record.prize_pool_impact = self.get_prize_pool_impact()
        record.save()
        super(Scraper, self).__init__()

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
        r = requests.get(url)
        return r.json()['data']['values'][DAU_EVENT][YESTERDAY]

    def get_revenue(self):
        REVENUE_EVENT = 'Revenue Collected'
        params = {
            'api_key': API_KEY,
            'expire': EXPIRE,
            'event': REVENUE_EVENT,
            'from_date': YESTERDAY,
            'to_date': YESTERDAY,
            'on': 'number(properties["amount"])',
            'limit': 1000
        }
        params['sig'] = self.hash_args(params)
        url = '/'.join([ENDPOINT, str(VERSION)]) + '/segmentation/sum?' + self.unicode_urlencode(params)
        r = requests.get(url)
        return r.json()['results'][YESTERDAY]

    def get_prize_pool_impact(self):
        EVENT = 'Score Challenge Closed'
        params = {
            'api_key': API_KEY,
            'expire': EXPIRE,
            'event': EVENT,
            'from_date': YESTERDAY,
            'to_date': YESTERDAY,
            'on': 'number(properties["prize pool impact"])',
            'limit': 1000
        }
        params['sig'] = self.hash_args(params)
        url = '/'.join([ENDPOINT, str(VERSION)]) + '/segmentation/sum?' + self.unicode_urlencode(params)
        r = requests.get(url)
        return r.json()['results'][YESTERDAY]

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
