from base import ObjectBase , CollectionBase
from datetime import datetime
from json import loads

class NotificationLogs(CollectionBase):
    ''' find() Return collection of Activity

        **  parameter application is required
    '''
    find_valid_constrains = ['format','offset','limit', 'order_by','application']
    findOne_valid_constrains = ['format','user', 'id'] ## not allowed any constrain
  
    def __init__(self, key,secret,host,app_id):
        self.consumer_key = key                                              
        self.consumer_secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        params['application'] = self.app_id
        meta, items = self._find("notification_log",params)
        notification_logs=[]
        for item in items:
            activity = NotificationLog(self.consumer_key, self.consumer_secret, self.host, item)
            notification_logs.append(activity)    
        return meta, notification_logs
    
class NotificationLog(ObjectBase):
    '''
        
         
    '''
    def __repr__(self):
        return '<log id: %s>'%(self.id)

    def __init__(self, key, secret, host, log):
        '''
            new cert using app_dict = {}, id = 0
        '''
        self.host = host
        self.consumer_key = key
        self.consumer_secret = secret
        if type(log)==int:
            self.id = log
            self.get()
        elif not log:
            self.id = None
        else:
            self.id                 = int(log.get('id','0'))                
            self.resource_uri       = log.get('resource_uri','')
            self.created            = datetime.strptime(log.get('created',None), '%Y-%m-%dT%H:%M:%S')
            self.message            = log.get('message','')
            self.application        = log.get('application','')
            self.meta               = loads(log.get('meta',"{}"))
            self.to_users           = loads(log.get('users', "[]"))     ## String in "[]" format.
            self.progress           = self.__get_progress(log.get('progress',[]))
            self.errors             = log.get('errors',[])

    def to_dict(self, params={}):
        return self.__dict__
                                
    def get(self):
        '''
            Get available notifications log entries
        '''
        log = None
        if self.id:
            params = {'id': self.id}
            log = self._get('notification_log',item_id=self.id, params= params)
            self.__init__(self.consumer_key, self.consumer_secret, self.host, log)
        return self
    
    def __get_progress(self, progress):
        if len(progress) > 0:
            for p in progress:
                try:
                    p["updated"] =  datetime.strptime(p["updated"], '%Y-%m-%dT%H:%M:%S')
                except: #backwards compatible to old timestamp format
                    p["updated"] =  datetime.strptime(p["updated"], '%Y-%m-%d %H:%M:%S+0000')
        return progress
            
           
        
