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
    def test_filtering_apps(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_filtering_apps
        '''
        app = self.partner.applications()
        meta , apps = app.filter_by_id(ids=[42,43])
        self.assertEqual( len(apps) ,2)
        self.assertIn( apps[0].id , [42,43])
        self.assertIn( apps[1].id , [42,43])
    
    def test_get_app_by_id(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_get_app_by_id
        '''
        app = self.partner.application(app=app_id)
        app.refresh()
    
    def test_filter_app_by_contains_package_name_or_appstore_id(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_filter_app_by_contains_package_name_or_appstore_id
        '''
        applications = self.partner.applications()
        params = {"contains_store_id":1}
        meta , apps = applications.findAllSocialize(params)
        self.assertTrue( len(apps) > 1)
        for app in apps:
            self.assertEqual( app.is_socialize_editable, True) 
            self.assertNotEqual( app.socialize_consumer_secret, None) 
            self.assertTrue( app.android_package_name or app.apple_store_id)                                                                               

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
        self.assertEqual( app.android_market_url(), "http://play.google.com/store/apps/details?id=%s" % app.android_package_name)
        

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

    def test_app_get_custom_domain(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationReadOperations.test_app_get_custom_domain
        '''
        apps = self.partner.applications(user_id)
        print app_id
        app = apps.findOne(app_id)
        app.custom_propagation_domain = "test.domain.com"
        app.save()

        apps = self.partner.applications(user_id)
        app_with_custom = apps.findOne(app_id)

        print str(app_with_custom.custom_propagation_domain) + "::"

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
            self.assertEqual( l.errors, [] )

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
        print "got applications"
        app = applications.findOne(app_id)
        print "got application (1)"
        message = "hello test from sdk \'developer_direct_entity\'"
        resp = app.send_notification(message, entity_id=1,user_id_list=[] ,subscription="developer_direct_entity")
        print "Sent notification"
        print "Response: ", resp
                                                                         
    def test_upload_p12_dev(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_upload_p12_prod

        '''
        ## UPload to deleted app
        applications = self.partner.applications(user_id)
        app = applications.findOne(delete_app)
        #print delete_app


        p12_base64 = """
        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
        """

        p12_password = 'asecretpassword'                    
        resp = app.upload_p12(p12_base64=p12_base64,
                key_password=p12_password)


        #print resp
        self.assertTrue(resp)
        cert = app.get_iphone_certificate()        
        self.assertEqual( cert.type, 'Development')

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





