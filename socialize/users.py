from base import ObjectBase , CollectionBase
from datetime import datetime

class ApiUsers(CollectionBase):
    '''
        find a list of api users in application
    '''
    def __init__(self, key,secret,host,app_id):
        self.key = key                                              
        self.secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        params['application_id'] = self.app_id
        meta, items = self._find('apiuser',params)
        api_users=[]
        for item in items:
            api_user = ApiUser(self.key, self.secret, self.host, item)
            api_users.append(api_user)    
        return meta, api_users
    
    def findOne(self, api_user_id, params={}):
        '''
            findOne doesn't care about application_id
        '''
        item = self._findOne('apiuser',api_user_id, params)
        api_user = ApiUser(self.key, self.secret, self.host, item)
        return api_user 

    def findBanned(self, params={}):
        params['application_id'] = self.app_id
        meta, items = self._find('apiuser',params, verb='banned')
        api_users=[]
        for item in items:
            api_user = ApiUser(self.key, self.secret, self.host, item)
            api_users.append(api_user)    
        return meta, api_users
 

class ApiUser(ObjectBase):
    '''
        find a single user from API
        ** API should allow filter by id & application
    '''
    def __repr__(self):
        return '<api_user id: %s ,first_name: %s>'%(self.id, self.first_name)

    def __init__(self, key,secret,host,api_user={}):
        '''
            new app using app_dict = {}, id = 0
        '''
        self.host = host
        self.key = key
        self.secret = secret
        if type(api_user)==int:
            self.id = api_user
            self.refresh()
        else:                      
            self.id                  = int(api_user.get('id','0'))                
            self.resource_uri        = api_user.get('resource_uri','')      
            self.created             = datetime.strptime(api_user.get('created',''), '%Y-%m-%dT%H:%M:%S')           
            self.updated             = datetime.strptime(api_user.get('updated',''),'%Y-%m-%dT%H:%M:%S')        

            self.date_of_birth       = api_user.get('date_of_birth','')    
            self.description         = api_user.get('description','')       
            self.device_id           = api_user.get('device_id','')         
            self.email               = api_user.get('email:null','')        
            self.first_name          = api_user.get('first_name','')        
            self.large_image         = api_user.get('large_image','')       
            self.last_name           = api_user.get('last_name','')         
            self.location            = api_user.get('location','')          
            self.medium_image        = api_user.get('medium_image','')      
            self.sex                 = api_user.get('sex','')               
            self.small_image         = api_user.get('small_image','')       

    def to_dict(self):
        return self.__dict__
                                
    def refresh(self):
        '''
            update object
        '''
        new_item = self._get('apiuser', self.id)
        self = self.__init__(self.key, self.secret, self.host, new_item) 
    
    def ban(self, app_id):
        '''
            ban current user 
            payload require app_id because api_user_id can be in multiple app with 3rdPartyAuth
            return True when success / else raise Exception
        '''
        payload = {'application_id': app_id}
        return self._post('apiuser',payload=payload, item= self.id, verb='ban')

    def unban(self, app_id):
        '''
            ban current user 
            payload require app_id because api_user_id can be in multiple app with 3rdPartyAuth
            return True when success / else raise Exception
        '''
        payload = {'application_id': app_id}
        return self._post('apiuser',  payload, item=self.id, verb='unban')
     
        
