try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, api_user_id
except:
    print 'unable to load local settings using-> settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app ,api_user_id

from socialize.client import Partner
from tests.base import SocializeTest

#class ApiUserTest(SocializeTest):

    #'''
        #find()
    #'''   
    #def xtest_get(self):
        #'''
            #** get api_user by api_user_id
        #'''
        #api_user = self.partner.api_user(api_user_id)
        #self.assertEqual( int(api_user.id) , api_user_id)
        #self.assertTrue( len(api_user.device_id) > 0)

