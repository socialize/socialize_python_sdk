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
from base import SocializeTimeTest

class AnalyticTest(SocializeTimeTest):
    '''
        find()
    '''   
    def test_init(self):
        '''
            ** test init analytic by app_id
            nosetests -s -v tests.analytic_test:AnalyticTest.test_init

        '''
        analytic = self.partner.analytics(app_id)
        self.assertEqual(analytic.app_id , app_id)
    
    def test_analytic_find_day(self):
        '''
            nosetests -s -v tests.analytic_test:AnalyticTest.test_analytic_find_day

        '''
        analytic = self.partner.analytics(app_id) 
        response = analytic.find()
        daydiff = 60 * 60 * 24 * 1000
        ## default to day
        for item in response:
            print item, response[item]
            self.assertTrue( len(response[item]) > 0)
            self.assertEqual( response[item][2][0] - response[item][1][0] , daydiff)

    def xtest_analytic_find_week(self):
        '''
            nosetests -s -v tests.analytic_test:AnalyticTest.test_analytic_find_week
        '''
        params = {'time_interval': 'week'}
        analytic = self.partner.analytics(app_id) 
        response = analytic.find(params)
        
        weekdiff =  60 * 60 * 24 * 7* 1000
        for item in response:
            #print item, response[item]
            self.assertTrue( len(response[item]) > 0)
            ## by week diff time = 60 * 60 * 24 * 7
            self.assertEqual( response[item][2][0] - response[item][1][0] , weekdiff)

