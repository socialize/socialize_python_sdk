import sys, os
cmd_folder = os.path.dirname(os.path.abspath(__file__)[-len('tests')])
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, api_user_id
except:
    print 'Failed to load local_settings.py. Switching to settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app , api_user_id

from socialize.client import Partner
from base import SocializeTest

class ApiUserTest(SocializeTest):

    '''
        find()
    '''   
    def test_init(self):
        '''
            ** test init api_user by api_user_id
            _install/bin/nosetests -s -v tests.api_user_test:ApiUserTest.test_init

        '''
        api_user = self.partner.api_user(app_id, api_user_id)
        self.assertEqual(int(api_user.id) , api_user_id)

    def test_find(self):
        '''
            ** test get list of api_users by app_id
        '''
        api_users = self.partner.api_users(app_id=5)
        meta, collection = api_users.find()
        
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            print item

    def test_findOne(self):
        ''' 
            ** test get single api_user_id object
        '''
        app_id = 5
        user_id = 210
        api_users = self.partner.api_users(app_id=app_id)

        api_client = api_users.findOne(api_user_id=user_id)

        self.assertEqual(int(api_client.id), user_id)
        
        print api_client.to_dict()

    def test_ban_user_by_app_and_id(self):
        '''
            ** test ban user from single app
        '''

        app_id = 5
        user_id = 5
        api_users = self.partner.api_users(app_id=app_id)

        api_client = api_users.findOne(api_user_id=user_id)

        resp = api_client.ban(app_id)
        self.assertTrue(resp)


    def test_ban_user_by_id(self):
        '''
            ** test ban user from user_id
            _install/bin/nosetests -s -v tests.api_user_test:ApiUserTest.test_ban_user_by_id
        '''
        print app_id, api_user_id
        api_user = self.partner.api_user(app_id, api_user_id=api_user_id)
        #print api_user.to_dict()
        resp = api_user.ban(delete_app)
        self.assertTrue(resp)    

    def test_find_list_banned_users(self):
        '''
            ** test find list of banned users
        '''
        api_users = self.partner.api_users(app_id = delete_app)
        meta, banned_list = api_users.findBanned()
        print meta
        print banned_list
        self.assertTrue(len(banned_list)>=1)
        
    def test_unban_user_by_id(self):
        '''
            ** test unban user from user_id
        '''
        print app_id, api_user_id
        api_user = self.partner.api_user(app_id, api_user_id=api_user_id)
        print api_user.to_dict()
        resp = api_user.unban(app_id)
        self.assertTrue(resp)     
