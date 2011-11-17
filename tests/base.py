import unittest
from socialize.client import Partner
try:
    from local_settings import version, host, key, secret, user_id , app_id
except:
    from settings import version, host, key, secret, user_id , app_id   

import os.path as op
TESTS_ROOT_PATH = op.dirname(op.realpath(__file__))
class SocializeTest(unittest.TestCase):
    RESOURCES_PATH = '%s/resources' % TESTS_ROOT_PATH
    
    def setUp(self):
        self.partner = Partner(key,secret,host)

    def tearDown(self):
        pass
