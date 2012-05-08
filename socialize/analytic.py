from utils import smart_str
from base import CollectionBase, ObjectBase
from datetime import datetime

class Analytics(CollectionBase):
    ''' find() Return collection of Analytic (Graph) on dashboard
        params: 
        -application_id (optional): Filters result set to a specific application.
        -activity_types (optional) : A comma-separated string from choices [comments, likes, shares, views]. Defaults to "comments, likes, shares, views".
        -distribution (optional): Choices are [cumulative, progressive]. Defaults to 'progressive'.
        -user_id (optional): Filters result set to a specific user.
        -time_interval (optional): Choices are [day, week, month]. Defaults to 'day'.
        -start_date (optional): Starting date for stats in format 'YYYY-MM-DD'. If unspecified, then intelligent guess is made based on timeframe.
        -end_date (optional): Ending date for stats in format YYYY-MM-DD. If unspecified, then intelligent guess is made based on timeframe.
    '''
    find_valid_constrains = ['application_id','start_date','end_date','activity_types',
                            'distribution','time_interval','user_id']
 
    def __init__(self, key,secret,host,app_id):
        self.consumer_key = key                                              
        self.consumer_secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        '''
            return list of stats base on time_interval
        '''
        params['application_id'] = self.app_id
        response = self._request('analytic' ,params)
        return response
