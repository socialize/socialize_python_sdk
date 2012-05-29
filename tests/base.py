import unittest
import datetime
from socialize.client import Partner
from json import loads, dumps
try:
    from local_settings import version, host, key, secret, user_id , app_id, timeout
except:
    from settings import version, host, key, secret, user_id , app_id, timeout

import os.path as op
from time import time
TESTS_ROOT_PATH = op.dirname(op.realpath(__file__))

class SocializeTest(unittest.TestCase):
    RESOURCES_PATH = '%s/resources' % TESTS_ROOT_PATH
    
    def setUp(self):
        self.partner = Partner(key,secret,host)

    def print_json(self, data):
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        txt = dumps(data, indent = 4,default=dthandler)
        print txt


class SocializeTimeTest(SocializeTest):
    RESOURCES_PATH = '%s/resources' % TESTS_ROOT_PATH
    
    def setUp(self):
        self.partner = Partner(key,secret,host)
        self.start = time() 

    def tearDown(self):
        #time usage
        self.time_usage = time() - self.start 
        #print "time usage: %s" % self.time_usage
        #print "time out: %s" % timeout
        self.assert_( self.time_usage < timeout, 'Timeout Exceed %f | from %f'%(self.time_usage, timeout))
