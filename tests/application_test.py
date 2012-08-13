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
        app = applications.findOne(app_id)
        message = "hello test from sdk \'developer_direct_entity\'"
        resp = app.send_notification(message, entity_id=1,user_id_list=[] ,subscription="developer_direct_entity")
        print "Response: ", resp
                                                                         
    def test_upload_p12_prod(self):
        '''
            nosetests -s -v tests.application_test:TestApplicationWriteOperations.test_upload_p12_prod

        '''
        ## UPload to deleted app
        applications = self.partner.applications(user_id)
        app = applications.findOne(delete_app)
        #p12_filename = '%s/%s' % (self.RESOURCES_PATH, 'simple-sample-prod.p12')

        #p12_content = open(p12_filename, 'rb').read()
        p12_base64 = '''
        MIIMkwIBAzCCDFoGCSqGSIb3DQEHAaCCDEsEggxHMIIMQzCCBq8GCSqGSIb3DQEHBqCCBqAwggacAgEAMIIGlQYJKoZIhvcNAQcBMBwGCiqGSIb3DQEMAQYwDgQIaS/ARh9u3zsCAggAgIIGaFenYz09r+fZzstgLMemKAq+SJmdswgWxGx+FJpXt3Y+PW1macV2whHeDVnNbRi29Ejgyax5XnBDbzVSyabSvGbGtHUOj0hPbOJ7NeIRC9SC3R9oZgHQaE1PPWEZO7wpnzJXWRYwFTjtqIVijfNJY2oyrGfIDLn6tpyqzKnpOH9oBl8tzLsIEXTsqLd6PMdMxkxcBQf2cv40+EMf7T5K9FgjXQ4kWXifc9oGeCTseBjM2WgeWG/BxCrP8GZ1Llt0CqrjUtlfDCksM3uKAUZKdOPd1uDYaDLpRpGaUddr0EjpXFn1vtDHjA5rDlWH+lNregOzyf7Um/1FYy4m9IbU9itYbp28o6NmhEuZXrZUyOYDKgZew6sUkrb0dXjsikxHH8X3umktzJHdsgK5JWcqtfZ4Z1QYoaMkblXIP20h6PT1YubNG/4UZPmttckefn7+f/jMZJ+V47uUEESPqaIB9Nrv1c270B2pUgjWsTlTJL9njk+3yvjqnXcFOOeBhwTRBuLgsqu92IE8LcoGczhGog7dvvW7JON171a5BE6lE3hmXataVGo5eru8e/4LsGqK94XwmMZIdCPCIpigZX2OQrMcsLEXTEGJZ7kr8rdwYgKsvE6OOAdZ8pICfzkCRasPd4/tR8zEUXml4XjbnqLfLHhQD0Yhk5wGbpzYSK6VxUi9D2PmARfTSO0m7WfODCHyuWYgrGcYCkh4c7PV/2dvbvCJTFLIU8I+zgbvR9Ya6fetho84qQyHgT8gsVjpcAn/egbXZMAJlnxIbqkjF+eSBc6zPqX2+J80PEaV+sLOc8bM5cApW1riKDqXN6u2WRwSGSwmTVyQXIt6y1nBn06Cbd0TNCdFea0lmXsuDzXUZW9muv2l1Y9s9TwJlRlvMAl0wol3JtU+gy415ea0rzaMzXZV2f36Iv2g4Og6KQskvdX9TvfmVFxgGigfOtQAiTtbb9RftTgf0SaYr3x2GlcT8d8IzMAPMqfbHlNhjwlGMhObUlbYAnDosd+xVsmUdApsPyAt1KWfT15J5O77Yzy0scFJG2ZPSodQrglVn8J3V5Sg/ji0WnSSWVOBM8BuBoN7ZCZZpBGg7oN3p/GurxaJK/lH+UGtX+NzNktkp8q8oZwH0Lflwph3F3tKldLY4FgBiO2jhuiux6vJi69FhhInELC9wx5giRD7bnc4CuKuS4C8NSDpu6vWQM8jRzcByaoOTKExsDjOpyRO3/GTDVJbARtEKAYr+sB8wRh6nFVHwm2P4ZmbeE1OuJzo6GHLK3kzTfEp3JsiYcFjE+koYuZUPMbw7pia4ZdmOvkFlPGd3FDfASJ+ep2c6kwe5QLdDqQ3mBAhlMvQUvuUhbDfHFWsWLWDA2IjQlcksO1fYEoyW/1rWemQHqR2V075lYoHOrWCASZM9eqMiKDYYoWfAGmdxc6i5+lL6oxjEWASlcjtO5UvewgjtVmd06oSE9cNMN3zzUY1zW+p3nq6S7twn23qTDYBWXGXshxVu3/GdbtsHoeFWu+uFXreKrePD8V/GQhwjzUwVQ1R9j0+exU3A7DCKQdfjfqnuiwg/AUaeXfWz2mLddI4iSYm3dNH6mIijgrZ5bkKeS28PRqEHgQ94+sbGH5PmAiGn0riBs8A7Z8tkUGcw6ngaUOAsK2zQ56FyulDXQYxrqA49PFaT4bg6gahE0AEVYuoCmOP44Vnn0Fd0csVs/H8ZOHT41hSU0iu+RNVvncwUUHl4rYnqxkMsK/Zi0in13Yymwp4Hxs2ae8HREagUpBD6TjoY1SPshWt24meyPu2wp2d5gIDIu8R4E8GYSfessBH1n5ErSOeUGF8nVTX2pjCHGfuWZ7Qf0bIl0N+4IwY9Ihozr4QHiiHuxH1M3wmgLnwZQL2GfrEY2F5Kg/bXdzmAHUvpwzrAgsRRXLeIMVVOhAmTIbFAxc7T6TQNbINhvwAx3tYsbzVYH+pzQLRySk/tS25XujdRqGxO2Lk1SB1QqJwgKfN6OxFTkUZIipsVc+W34CKaG82Ejf92KUPijzb/0WjMFLW2gLvbB36hTibPqYbVStmySItwgOhy/HhXYHfEA7XmnhNJb0EJEiGRWhEiU65bP4VMxTtK9Ydt+arlem0UIbVXu07syTJ/jrN2joUizZk0ggCyJXKRH9nZK3l+9HYvrSmt/+iWmqIgQbxScsiP6dQMIIFjAYJKoZIhvcNAQcBoIIFfQSCBXkwggV1MIIFcQYLKoZIhvcNAQwKAQKgggTuMIIE6jAcBgoqhkiG9w0BDAEDMA4ECJDihJfBO/HSAgIIAASCBMh6VyHKVgH0emoijlK8Kfh6QeuHE+2R/Or+VqD5jO0KzEmBJu8tix5QYNMaS1UQfNDlQKILHwB++dtI/w5FzF9Ai1Ic5Ckk2SS/qu9uZIZEacBP0m3cstSnccNcrlaG3MnpPffnmepsPlkh4k4E7lRzu8ibsbOWJdbow4jpEiaD3CC0q2TeihrdER/GZZEt+i9xAKy6GFKuUlPRt0LCuoEhGQUzUDVPW1Owldy5y05YxgX11eORYB8AJNidkGTh0ACm37oSg2GGQhcLtzZ3KTdBEJ71bmSQEujDszROl1/Y+qov7sdIfh8YZ/wyBJTUS/tQdAVtp6Ky0K12H4xUXcT9NY6uhzwXvvPwhxvhoIosuEsFg0gQqJ8CJ3sZOMHQVviLfq5Q12iEJ/fjmuZM0FFpoDj6ZRxZAODitj2d9/t3/H7OmSfNerZiRbBYfbgjR1zI3EdwWg6e4IFLkdT5uUlO21NtEFpDsWUKCFiBT+ByBrl/uWE7x9lb7TOpYz35pdacVp5lHCPxfdXk37A8sTVF52nE90AOS/NW5PRxWvGocSt/LEppwPPhtTnZTMGIL4Aj8UQkWUMesLb0rc3lhmpE2lXopE87Pb40Kw65LqnmtILIfMalk9gqTitOtpXJ0KRd5sCfhRtfzTNlxS4bXF4w1nfpMZpB/yeTdQJy4nWc+ZqA0I5O1AO3UrdbLDwtzAkQ9Q+v8NSy04Ejm/v6Ks647ih69rmrAWcrgNKiGrvbcLKNgsAAdzsVlylUDQtgyq4p4DwT/Hrok4HowwtmJfzvjTj7r0+sA1EjbYxKPZ6Voa4yz8CvTefKjgZ+PA6+wIZb8aY/Sml7F6/u1wks4pI/BlTQCUZFUMJLepM/X5ZPIivjo5u3sr9v/qEnC8GSIv9nXmIc2U3T6AJsNRRj4RyafZ4VVJcHiu1HVUJgwwe6yfXfip7DpoogAhmYTpZITfulhrbt7g0BGNEQKeudRnyM81Xt12wPhMOaBa7BCWAeBVRsfajo4fbt20g1XNnn+sNa151ckENmdTUx9ELKCdhjiCRWJlPtUL9crpjJIb9sXGNHIVBWRDHGoMht2ydiEB51T/c6s4EpDgZkvNsWdnWF7MDOKaR4aNl8gm2DSSFVUVGlDhvEPEc2yCjcmZeApPqWSeOgxDc1/1jaF9b1QS/fq+/ZyJLAT4zfqzQTa9wDEx5Ce0MSrD0QqNJ5ruzxA3IcZyZYx0SQQFW1ieGNIxYMkGl8GAHW67MhCj4NbmuCRi7zZr1TJAT1VQhJOTRhH1ZWDhpd/RiDVfXSjSEOM8FMoPrk/8K4zrU5pLL+ac50cBwAu8rSIUQ62LUn0QJ5ht1qwJn9VT3l5th8oApC9J1MHWwkqPeVhu7pFuCfVgKBJnZ4ZLqOBpfFurjzGW3km1F/pFEQmgG8ESXIsQyX4vc1+D6djXG2D35L1HIJZzCgGdmVrB9sTTl+PkzUXj/IKlQLtBRkPrAbNyd9M45eBJfp4ZTHXzqHkix+/C3H7LR+83nCVr88dJSvaPF47+Iz1sUJTS5QJta0mG7/f+NjaFZEZe9RrcH5SvvjFV0eaDQC4JqI/T7DNh9C9kMd9q740EAhK0X0Y6yM4bOpn1OYiXRX8PZEoJlD0MsxcDBJBgkqhkiG9w0BCRQxPB46AFMAaQBtAHAAbABlACAAUwBhAG0AcABsAGUAIABQAHIAbwBkAHUAYwB0AGkAbwBuACAAUAB1AHMAaDAjBgkqhkiG9w0BCRUxFgQUjnP1DjiCTFrRErOSB5xn6GiMJPQwMDAhMAkGBSsOAwIaBQAEFAGXtt3JaUTg9yoLXFj6kk1IX3EABAhCjluXCfblmgIBAQ==
        '''
        p12_password = 'b3s0cial'                    
        resp = app.upload_p12(p12_base64=p12_base64,
                key_password=p12_password)
        self.assertTrue(resp)
        cert = app.get_iphone_certificate()        
        self.assertEqual( cert.type, 'Production')

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





