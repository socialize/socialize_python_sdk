import sys, os
cmd_folder = os.path.dirname(os.path.abspath(__file__)[-len('tests')])
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)    
sys.path.append('..')
sys.path.append('.')
try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app
except:
    print 'Failed to load local_settings.py. Switching to settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app

from socialize.client import Partner ,Applications, Application
from base import SocializeTest
from time import sleep
import base64

class TestApplicationReadOperations(SocializeTest):
    '''
        find(), findOne(),
    '''   
    def test_collections_get(self):
        '''
            ** get applications by user in database
        '''
        apps = self.partner.applications(user_id)
        meta, result = apps.find()

        self.assertTrue(meta['total_count'] > 0)
        for app in result:
            self.assertEqual( app.user,user_id)
        
    def test_collections_get_with_params(self):
        '''
            ** get collection of applications with parameters
        '''
        apps = self.partner.applications(user_id)
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
        apps = self.partner.applications(user_id)
        
        params = {'invalid param':'xox'}
        try:
            meta, result = apps.find(params) 
        
        except Exception as e:
            self.assertTrue( e[0].startswith('parameter'))

    def test_app_get(self):
        '''
            ** get single application object by app-id using findOne()
        '''

        apps = self.partner.applications(user_id)

        ## get specific app id
        app = apps.findOne(app_id)
        self.assertEqual( app.id , app_id)
        self.assertTrue( app.name != '')
        
        ## show Application Object <id: 240754 ,name: test_app>
    def test_app_obj(self):
        '''
            ** return valid type of object
        '''
        apps = self.partner.applications(user_id)
        self.assertEqual( type(apps), Applications)

        new_app = self.partner.application()
        self.assertEqual( type(new_app), Application)

        app = apps.findOne(app_id)
        self.assertEqual( type(app), Application)

    def test_new_apps(self):
        '''
            ** test two ways of creating new application
        '''
        new_app = self.partner.application()
        self.assertEqual( type(new_app), Application)

        apps = self.partner.applications(user_id)
        new_app2 = apps.new()

        self.assertEqual( type(new_app), type(new_app2))
        self.assertEqual( new_app, new_app)
    
    def test_find_api_users(self):
        '''
            ** test list user from application
            _install/bin/nosetests -s -v tests.application_test:TestApplicationReadOperations.test_find_api_users
        '''

        apps = self.partner.applications(user_id)
        app = apps.findOne(app_id)
        meta, users = app.list_api_users()
        self.assertNotEqual( len(users), 0 )
        for user in users:
            self.assertNotEqual(user.id ,0) 
        

class TestApplicationWriteOperations(SocializeTest):
    '''
        save() , update(), delete()
        This test has been disable by QA 
        you can include this test in __init__.py
        or run specific using nosetests 
    '''
    
    def test_write_flow(self):
        '''
            ** test create app then edit the app, then refresh()
        '''
        
        app_id = self.create_app()
        self.update_app(app_id)
        self.test_delete_app(app_id)
    def create_app(self):
        applications = self.partner.applications(user_id)
        app =  applications.new()
        
        ## app id =0 before save()
        self.assertTrue(app.id==0)
        
        app.name='The newest Socialize App'
        app.desc='Test application from python sdk'
        app.mobile_platform=['iPhone','android', ]
        app.category = 'Business'
        ## need to assign to specific user
        app.user = user_id
        app.save()
        ## app id will be obtain after save()
        self.assertTrue(app.id>0)

        ## get that app from api
        app.refresh() 

        self.assertTrue(app.last_saved != '')
        return app.id

    def update_app(self,app_id):
        applications = self.partner.applications(user_id)
        app =  applications.findOne(app_id)            

        previous_save_time = app.last_saved        
        new_name = 'Change name to new name'
        #print app.to_dict()
        app.name= new_name
        ## update if app already have an id
        sleep(1)
        app.save()
        app.refresh() 
        self.assertEqual(app.name,new_name)
        self.assertTrue(app.last_saved != previous_save_time)

    def test_delete_app(self,delete_app = delete_app):
        '''
            ** test Application DELETE 
        '''
        applications = self.partner.applications(user_id)
        app = applications.findOne(delete_app)
        ## return True when succesfully delete
        resp = app.delete()
        self.assertTrue(resp)
        app = applications.findOne(delete_app)
        self.assertEqual( app.delete(), True)

    def test_applications_delete( self,delete_app = delete_app):
        '''
            ** Applications delete by app_id
        '''
        applications = self.partner.applications(user_id)
        resp = applications.delete(delete_app)
        ## return True when succesfully delete
        self.assertTrue(resp)

        applications = self.partner.applications(user_id)        
        app = applications.findOne(delete_app)
        self.assertEqual( app.delete(), True)  

    def test_upload_image_icon(self):
        '''
            Upload application_icon
        '''
        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        print app
        icon_filename = '%s/%s' % (self.RESOURCES_PATH, 'app_icon.png')
        icon_content = open(icon_filename, 'rb').read()
        icon_base64 = base64.b64encode(icon_content) 
        print len(icon_base64)
        resp = app.upload_icon( icon_base64)
        print "Response: ", resp
        self.assertTrue(resp)
    
    def test_set_notifications_enabled(self):
        '''
            Set notification_enabled to True
        '''
        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        print app
        resp = app.set_notifications_enabled(True)

        print "Response: ", resp
        app = applications.findOne(app_id)
        self.assertEqual( app.id , app_id)
        self.assertTrue( app.name != '') 
        self.assertEqual(app.notifications_enabled, True)
 
    def xtest_upload_p12(self):
        '''
            Upload p12 for push notification
        '''
        ## UPload to deleted app
        applications = self.partner.applications(user_id)
        app = applications.findOne(delete_app)
        p12_filename = '%s/%s' % (self.RESOURCES_PATH, 'new_certificate_pkey.p12')

        p12_content = open(p12_filename, 'rb').read()
        p12_base64 = base64.b64encode(p12_content)
        p12_password = 'success'                    
        resp = app.upload_p12(p12_base64=p12_base64,
                key_password=p12_password)
        self.assertTrue(resp)
