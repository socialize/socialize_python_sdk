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

    def test_get_notification_log(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_get_notification_log
        '''
        apps = self.partner.applications(user_id)
        app = apps.findOne(app_id)
        logs = app.get_notification_logs()
        for l in logs:
            print l.to_dict()

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
        
        app.name='The newest Socialize & App'
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
        self.assertEqual( app.c2dm_token_source, 'socialize')
        return app.id



    def update_app(self,app_id):
        applications = self.partner.applications(user_id)
        app =  applications.findOne(app_id)            

        previous_save_time = app.last_saved        
        new_name = 'Voice Band App & Co..'
        #print app.to_dict()
        app.name= new_name
        ## update if app already have an id
        sleep(1)
        app.save()
        app.refresh() 
        self.assertEqual(app.name,new_name)
        self.assertTrue(app.last_saved != previous_save_time)

    def test_update_app(self,app_id=app_id):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_update_app
        '''
        applications = self.partner.applications(user_id)
        app =  applications.findOne(app_id)            

        previous_save_time = app.last_saved        
        new_name = 'Change name to new  & name'
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
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_upload_image_icon
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


    def test_upload_p12(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_upload_p12
            Upload p12 for push notification
        '''
        ## UPload to deleted app
        applications = self.partner.applications(user_id)
        print delete_app
        app = applications.findOne(delete_app)
        p12_password = "b3s0cial"
        p12_base64= """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"""


        resp = app.upload_p12(p12_base64=p12_base64,
                key_password=p12_password)
        
        self.assertTrue(resp)


    def test_save_c2dm(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_save_c2dm
        '''
        pkg_name = 'com.champ.test'
        c2dm_token = "abcdefghijklmnop"

        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        app.android_package_name = pkg_name
        app.c2dm_sender_auth_token = c2dm_token
        app.save()
        
        print app.c2dm_sender_auth_token
        self.assertEqual( app.c2dm_sender_auth_token, c2dm_token)
        self.assertEqual( app.android_package_name ,pkg_name)
        
    def test_set_c2dm(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_set_c2dm
        '''
        pkg_name = 'com.champ.test'
        c2dm_token = "ABCXYXZ"

        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        app.android_package_name = pkg_name
        #print app.__dict__
        print app.c2dm_sender_auth_token
        app.save()
        #print app.__dict__
        app.set_c2dm_token(c2dm_token)
        print c2dm_token
        print app.android_package_name
        print app.c2dm_sender_auth_token

        
        app.refresh()
        print app.__dict__
        self.assertEqual( app.c2dm_sender_auth_token, c2dm_token)
        self.assertEqual( app.android_package_name ,pkg_name)
        self.assertEqual( app.c2dm_token_source, "developer") 

    def test_set_invalid_c2dm(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_set_invalid_c2dm
        '''
        pkg_name = ''
        c2dm_token = 'abcdefghijklmnop'

        applications = self.partner.applications(user_id)
        app = applications.findOne(app_id)
        app.android_package_name = pkg_name
        app.c2dm_sender_auth_token= c2dm_token
        try:
            app.save()
        except ErrorC2DMwithoutPackageName,e :
            self.assertEqual(e.content , "Need android package name in order to send smart alert")

    def test_create_app_with_ampersand_name(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_create_app_with_ampersand_name
        '''
        name = "test & test"
        pass
