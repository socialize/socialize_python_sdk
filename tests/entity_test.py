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
            nosetests -s -v tests.entity_test:EntityTest.test_entity_findOne
        '''

        entity = self.partner.entities(app_id)
        try:
            item = entity.findOne(9999999)
        except ErrorNotFound:
            pass
