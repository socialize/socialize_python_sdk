try:
    from local_settings import version, host, key, secret, user_id , app_id
except:
    from settings import version, host, key, secret, user_id , app_id
from socialize.client import *
from tests.base import SocializeTest


class PartnerTestRead(SocializeTest):
    '''
        find(), findOne(),
    '''
    def test_collections_get(self):
        '''
            ** get applications by user in database
        '''
        partner = Partner(key,secret,url=host)
        apps = partner.applications(user_id)
        meta, result = apps.find()

        self.assertTrue(meta['total_count'] > 0)
        for app in result:
            self.assertEqual( app.user,user_id)
        
    def test_collections_get_with_params(self):
        '''
            ** get collection of applications with parameters
        '''
        
        partner = Partner(key,secret,url=host)
        apps = partner.applications(user_id)
        
        params = {'format':'json',
                'offset':1,         ## start position
                'limit':4,          ## number of return per page
                'user':user_id,
                'order_by':'-created'}  ## order by created desc

        meta, result = apps.find(params)
        
        self.assertEqual(meta['offset'], params['offset'])
        self.assertEqual(meta['limit'], params['limit'])
        self.assertEqual(len(result), params['limit'])

    def test_collections_get_with_bad_params(self):
        '''
            ** get with bad params 
        '''
        partner = Partner(key,secret,url=host)
        apps = partner.applications(user_id)
        
        params = {'invalid param':'xox'}
        try:
            meta, result = apps.find(params) 
        
        except Exception as e:
            self.assertTrue( e[0].startswith('parameter'))

    def test_app_get(self):
        '''
            ** get single application object by app-id using findOne()
        '''
        partner = Partner(key,secret,url=host)
        apps = partner.applications(user_id)

        ## get specific app id
        app = apps.findOne(app_id)
        
        ## show Application Object <id: 240754 ,name: test_app>

class PartnerTestWrite(SocializeTest):
    '''
        save() , update(), delete()
        This test has been disable by QA 
        you can include this test in __init__.py
        or run specific using nosetests 
    '''
    
    def xtest_write_flow(self):
        app_id = self.create_app()
        self.update_app(app_id)
        self.delete_app(app_id)

    def create_app(self):
        partner = Partner(key,secret,url=host)
        applications = partner.applications()
        app =  applications.new()
        
        ## app id =0 before save()
        self.assertTrue(app.id==0)
        
        app.name='The newest Socialize App'
        app.desc='Test application from python sdk'
        app.mobile_platform=['iPhone','android']
        app.category = 'Business'
        ## need to assign to specific user
        app.user = user_id
        app.save()
        ## app id will be obtain after save()
        self.assertTrue(app.id>0)
        self.assertTrue(app.last_saved != '')
        return app.id

    def test_update_app(self,app_id):
        partner = Partner(key,secret,url=host)
        applications = partner.applications()
        app =  applications.findOne(app_id)            
        previous_save_time = app.last_saved        
        new_name = 'Change name to new name'
        app.name= new_name
        ## update if app already have an id
        app.save()
        self.assertEqual(app.name,new_name) 
        self.assertTrue(app.last_saved != previous_save_time)


#    def delete_app(self,app_id):
        #partner = Partner(key,secret,url=host)
        #applications = partner.applications()
        #app =  applications.findOne(app_id)
        #app.delete()
