import sys, os
cmd_folder = os.path.dirname(os.path.abspath(__file__)[-len('tests')])
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
from datetime import datetime
try:
    from local_settings import version, host, key, secret, user_id , app_id, delete_app, api_user_id, entity_id
except:
    print 'Failed to load local_settings.py. Switching to settings.py'
    from settings import version, host, key, secret, user_id , app_id, delete_app , api_user_id

from socialize.client import Partner
from base import SocializeTest
from socialize.base import Error, ErrorNotFound

class EntityTest(SocializeTest):
    '''
        find()
    '''   
    def test_init(self):
        '''
            ** test init entity by app_id
            nosetests -s -v tests.entity_test:EntityTest.test_init

        '''
        entity = self.partner.entities(app_id)
        self.assertEqual(entity.app_id , app_id)
    
    def test_entity_find(self):
        '''
            ** test get list of entity by app_id
        '''
        entity = self.partner.entities(app_id)
        meta, collection = entity.find()
        
        for item in collection:
            self.assertNotEqual(int(item.id) , 0)
            self.assertEqual(entity.app_id , app_id)
            print item.__dict__
       
    def test_entity_findOne(self):
        '''
           nosetests -s -v tests.entity_test:EntityTest.test_entity_findOne
        '''
        entity = self.partner.entities(app_id)
        item = entity.findOne(entity_id)
        self.assertNotEqual(int(item.id), 0 )
    
    def test_entity_NotFound(self):
        '''

            nosetests -s -v tests.entity_test:EntityTest.test_entity_NotFound
        '''

        entity = self.partner.entities(app_id)
        try:
            item = entity.findOne(9999999)
        except ErrorNotFound:
            pass

    def test_new_entity(self):
        '''
            nosetests -s -v tests.entity_test:EntityTest.test_new_entity
        '''           
        entity = self.partner.entities(app_id)
        e = entity.new()
        name = 'test entity by partner sdk'
        key  = 'http://getsocialize.com/test_sdk?hello=world&wt=123&fff=123123-e'
        
        e.name = name
        e.key = key
        self.assertEqual( e.application, app_id)
        self.assertEqual( e.name , name)
        self.assertEqual( e.key , key)
        self.assertEqual( e.id , 0)

        e.save()

        e.refresh()

        self.assertEqual( e.application, app_id)
        self.assertEqual( e.name , name)
        self.assertEqual( e.key , key)
        self.assertNotEqual( e.id , 0)    

        return e


    def un_test_save_and_delete_entity(self):
        '''
            nosetests -s -v tests.entity_test:EntityTest.test_save_and_delete_entity            
            ** stage server not support yet! wait for release 1.9.0
        ''' 
        e = self.test_new_entity()
        print e.__dict__
        e.save()

        print e.delete()
        try:
            entity = self.partner.entities(app_id)
            item = entity.findOne(e.id)
            self.fail(' should not able to find entity')
        except ErrorNotFound:
            pass

        
