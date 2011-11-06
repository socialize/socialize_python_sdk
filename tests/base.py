import unittest
from socialize.client import Partner
try:
    from local_settings import version, host, key, secret, user_id , app_id
except:
    from settings import version, host, key, secret, user_id , app_id   


class SocializeTest(unittest.TestCase):
    def setUp(self):
        self.partner = Partner(key,secret,url=host)

    def tearDown(self):
        pass
