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
        print app.to_dict()
    
#    def test_keep_fetch_socialize_apps(self):
        #'''
            #nosetests -s -v tests.application_test:TestApplicationReadOperations.test_keep_fetch_socialize_apps
        #'''
        #applications = self.partner.applications()
        #list_apps = []
        #limit = 50
        #offset = 0
        #params = {'limit':limit, 'offset':offset, 'show_total_count':1}
        #meta , apps = applications.findAllSocialize(params=params)
        #total_apps = meta['total_count']
        #list_apps = apps
        #while True:
            #offset += limit
            #params = {'limit':limit, 'offset':offset}
            #meta , apps = applications.findAllSocialize(params)
            #self.print_json(meta)
            #list_apps += apps
            #print len(list_apps)
            #if len(apps) < limit:
                #break

        #self.assertEqual( total_apps, len(list_apps))

    
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





