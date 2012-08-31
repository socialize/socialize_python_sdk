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
from socialize.users import ApiUserStat ,ApiUser
from socialize.base import ErrorNotFound
def create_user(**kwargs):
    user  = {
            "badges": [],
            "updated": "2012-01-07T05:35:43",
            "likes": 0,
            "devices": [],
            "created": "2011-09-01T00:00:00",
            "mo": "Voyeur",
            "views": 0,
            "secret": "46d212f7-17f4-464c-a9b1-679db3bc5d25",
            "comments": 0,
            "app_id": 240754,
            "application": 240754,
            "host": "http://stage.api.getsocialize.com",
            "score": 0.0,
            "user": {},
            "key": "747a34c9-a482-48a2-b946-4363cf9c8759",
            "is_banned": False,
            "total": 0,
            "id": 3215174,
            "shares": 0,
            "resource_uri": "/partner/v1/api_user_stat/3215174/",
            "third_party_auth":[],
        }
    for a in kwargs:
        user[a] = kwargs[a]
    return user
        

class ApiUserStatTest(SocializeTest):
    def test_init_stats(self):
        '''
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_init_stats

        '''
        api_user_stats = self.partner.api_user_stats(app_id)
        self.assertEqual(api_user_stats.app_id,app_id)
    
    def test_score(self):
        '''
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_score 
        '''
        score_list=[0]
        print 'start user'
        u = create_user( comments=1,shares=0,likes=0,views=10,)
        user = ApiUserStat(key='key',secret='secret',host='host',app_id=1,api_user_stat=u)
        print user.score
        score_list.append(user.score)

        print 'viewer'
        u = create_user( comments=1,shares=0,likes=0,views=400,)
        user = ApiUserStat(key='key',secret='secret',host='host',app_id=1,api_user_stat=u)
        print user.score         
        score_list.append(user.score)

        print 'inactive'
        u = create_user( comments=10,shares=1,likes=10,views=300, )
        user = ApiUserStat(key='key',secret='secret',host='host',app_id=1,api_user_stat=u)
        print user.score
        score_list.append(user.score)

        print 'active'
        u = create_user( comments=200,shares=100,likes=200,views=500)
        user = ApiUserStat(key='key',secret='secret',host='host',app_id=1,api_user_stat=u)
        print user.score
        score_list.append(user.score)
        print score_list
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
    def test_find_authd(self):
        """    
            nosetests -s -v tests.api_user_test:ApiUserStatTest.test_find_authd 
        """
        api_user_stats = self.partner.api_user_stats(384309)
        meta, stats = api_user_stats.authd_users()
        
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
        except ErrorNotFound, e:
            self.assertEqual(type(e), ErrorNotFound)  
            #self.assertEqual(e.message, 404)
 
        
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

#    def cancle_test_find_list_banned_users(self):
        #'''
            #API CANCLE THIS ENDPOINT as of v1.17.0
            #** test find list of banned users
        #'''
        #api_users = self.partner.api_users(app_id = delete_app)
        #meta, banned_list = api_users.findBanned()
        #print meta
        #print banned_list
        #self.assertTrue(len(banned_list)>=1)
        
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
