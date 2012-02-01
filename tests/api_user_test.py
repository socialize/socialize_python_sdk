import sys, os
cmd_folder = os.path.dirname(os.path.abspath(__file__)[-len('tests')])
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from datetime import datetime
try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, api_user_id
except:
    print 'Failed to load local_settings.py. Switching to settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app , api_user_id

from socialize.client import Partner
from base import SocializeTest


class ApiUserStatTest(SocializeTest):
    def test_init_stats(self):
        '''
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_init_stats

        '''
        api_user_stats = self.partner.api_user_stats(app_id)
        self.assertEqual(api_user_stats.app_id,app_id)

    def test_find(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_find 
        """
        api_user_stats = self.partner.api_user_stats(app_id)
        meta, stats = api_user_stats.find()
        
        self.assertTrue( len(stats) > 0)
        memory = []
        for item in stats:
            self.assertTrue( item.id not in memory)
            memory.append(item.id)
            
            print item

    def test_findOne(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_findOne 
        """
        api_user_stats = self.partner.api_user_stats(app_id)
        api_user = api_user_stats.findOne(api_user_id = api_user_id)
        self.assertEqual( api_user.user.id , api_user_id)
        print api_user

    def test_findOneNotFound(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_findOneNotFound 
        """
        api_user_stats = self.partner.api_user_stats(app_id)
        try:
            api_user = api_user_stats.findOne(api_user_id = 1)
        except Exception, e:
            self.assertEqual(type(e), Exception)  
            self.assertEqual(e.message, 404)
 
        
    def test_most_recent_users(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_most_recent_users 
        """
        api_user_stats = self.partner.api_user_stats(app_id)
        meta, recent = api_user_stats.most_recent_users()
        
        self.assertTrue( len(recent) > 0)
        memory = []
        prv_id = 0
        for item in recent:
            
            self.assertTrue( item.id not in memory)
            memory.append(item.id)

            
            self.assertTrue( prv_id <= item.id)

              
            prv_created  = item.id
 

    def test_most_active_users(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_most_active_users 
        """
        api_user_stats = self.partner.api_user_stats(app_id)
        meta, active = api_user_stats.most_active_users()
        
        self.assertTrue( len(active) > 0)
        memory = []
        prv_total = 9999999999999999999
        for item in active:
            
            self.assertTrue( item.id not in memory)
            memory.append(item.id)
            self.assertTrue( prv_total >= item.total)
            prv_created  = item.total

    def test_banned_users(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_banned_users 
        """
        api_user_stats = self.partner.api_user_stats(app_id)
        meta, active = api_user_stats.banned_users()
        
        self.assertTrue( len(active) > 0)
        memory = []
        for item in active:
            
            self.assertTrue( item.id not in memory)
            memory.append(item.id)
            self.assertTrue( item.is_banned)
            prv_created  = item.total

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


    def test_find_list_of_api_users(self):
        '''
            ** test find list of api user id=[28495552, 28494918]
            && len(response) = 2
        '''
        api_users = self.partner.api_users(app_id = app_id)


        pass 
