import sys, os
cmd_folder = os.path.dirname(os.path.abspath(__file__)[-len('tests')])
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)    
sys.path.append('..')
sys.path.append('.')
try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, socialize_consumer_key
except:
    print 'Failed to load local_settings.py. Switching to settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app,socialize_consumer_key

from socialize.client import Partner ,Applications, Application
from socialize.base import ErrorC2DMwithoutPackageName
from base import SocializeTest
from time import sleep
import base64

class TestApplicationReadOperations(SocializeTest):

    '''
        find(), findOne(),
    '''
    
    
    def test_get_app_by_id(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_get_app_by_id
        '''
        app = self.partner.application(app=app_id)
        app.refresh()
        print app.to_dict()
    
    def test_keep_fetch_socialize_apps(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_keep_fetch_socialize_apps
        '''
        applications = self.partner.applications()
        list_apps = []
        limit = 50
        offset = 0
        params = {'limit':limit, 'offset':offset, 'show_total_count':1}
        meta , apps = applications.findAllSocialize(params=params)
        total_apps = meta['total_count']
        list_apps = apps
        while True:
            offset += limit
            params = {'limit':limit, 'offset':offset}
            meta , apps = applications.findAllSocialize(params)
            self.print_json(meta)
            list_apps += apps
            print len(list_apps)
            if len(apps) < limit:
                break

        self.assertEqual( total_apps, len(list_apps))

    

    def test_find_all_socialize(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_find_all_socialize
        '''
        applications = self.partner.applications()
        meta , apps = applications.findAllSocialize()
        self.assertTrue( len(apps) > 1)
        for app in apps:
            self.assertEqual( app.is_socialize_editable, True) 
            self.assertNotEqual( app.socialize_consumer_secret, None) 

    def test_find_by_key(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_find_by_key
        '''

        apps = self.partner.applications(user=None, socialize_consumer_key=socialize_consumer_key)
        app = apps.findByKey()
        self.assertEqual( app.socialize_consumer_key, socialize_consumer_key) 
        self.assertNotEqual( app.socialize_consumer_secret, None) 
        
    def test_get_appstore_url(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_get_appstore_url
        '''
        apps = self.partner.applications(user_id)

        ## get specific app id
        app = apps.findOne(app_id)
        print app.appstore_url()     
        self.assertEqual( app.appstore_url(), "http://itunes.apple.com/us/app/id%s"%app.apple_store_id)

    def test_get_android_market_url(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_get_android_market_url
        '''
        apps = self.partner.applications(user_id)

        ## get specific app id
        app = apps.findOne(app_id)
        print app.android_market_url()     
        self.assertEqual( app.android_market_url(), "https://market.android.com/details?id=%s" % app.android_package_name)
        

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
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_app_obj

        '''
        apps = self.partner.applications(user_id)
        self.assertEqual( type(apps), Applications)

        new_app = self.partner.application()
        self.assertEqual( type(new_app), Application)

        app = apps.findOne(app_id)
        self.assertEqual( type(app), Application)

    def test_new_apps(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_new_apps
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
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_find_api_users
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
    def test_invalid_add_c2dm(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_invalid_add_c2dm
        
        '''
        applications = self.partner.applications(user_id)
        app =  applications.new()
        
        ## app id =0 before save()
        self.assertTrue(app.id==0)
        
        app.name='The newest Socialize App'
        app.desc='Test application from python sdk'
        app.mobile_platform=['iPhone','android', ]
        app.category = 'Business'
        app.c2dm_sender_auth_token = 'abc'
        ## need to assign to specific user
        app.user = user_id
        
        try:
            app.save()
        except ErrorC2DMwithoutPackageName,e :
            self.assertEqual(e.content , "Need android package name in order to send smart alert")

                               
    def test_write_flow(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_write_flow
            ** test create app then edit the app, then refresh()
        '''
        
        app_id = self.create_app()
        self.update_app(app_id)
        self.delete_application(app_id)

    def create_app(self):
        applications = self.partner.applications(user_id)
        app =  applications.new()
        
        ## app id =0 before save()
        self.assertTrue(app.id==0)
        
        app.name='The newest Socialize App'
        app.desc='Test application from python sdk'
        app.mobile_platform=['iPhone','android', ]
        app.category = 'Business'
        app.android_package_name = 'com.socialize.test'
        ## need to assign to specific user
        app.user = user_id
        app.save()
        ## app id will be obtain after save()
        self.assertTrue(app.id>0)
        self.print_json(app.__dict__)
        
        ## get that app from api
        app.refresh() 
        self.print_json(app.__dict__)

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

    def delete_application(self,delete_app):
        '''
            ** test Application DELETE 
            v1.17.0 
            application endpoint no longer return deleted app
        '''
        applications = self.partner.applications(user_id)
        app = applications.findOne(delete_app)
        ## return True when succesfully delete
        resp = app.delete()
        self.assertTrue(resp)
#        app = applications.findOne(delete_app)
        #self.assertEqual( app.delete(), True)

#    def test_applications_delete( self,delete_app = delete_app):
        #'''
            #** Applications delete by app_id
        #'''
        #applications = self.partner.applications(user_id)
        #resp = applications.delete(delete_app)
        ### return True when succesfully delete
        #self.assertTrue(resp)

        #applications = self.partner.applications(user_id)        
        #app = applications.findOne(delete_app)
        #self.assertEqual( app.delete(), True)  

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
    
    def test_send_developer_notification(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_send_developer_notification
            send notification subscription: "developer_notification"
        '''
        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        message = "hello test from sdk \'developer_notification\'"
        resp = app.send_notification(message, entity_id=1,user_id_list=[] ,subscription="developer_notification")
        print "Response: ", resp

    def test_send_developer_direct_entity(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_send_developer_direct_entity
            send notification subscription: "developer_notification"
        '''
        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        message = "hello test from sdk \'developer_direct_entity\'"
        resp = app.send_notification(message, entity_id=1,user_id_list=[] ,subscription="developer_direct_entity")
        print "Response: ", resp
                                                                         
    
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
