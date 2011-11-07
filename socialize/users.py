from base import ObjectBase


class ApiUser(ObjectBase):
    '''
        find a single user from API
        ** API should allow filter by id & application
    '''
    def __repr__(self):
        return '<api_user id: %s ,first_name: %s>'%(self.id, self.first_name)

    def __init__(self, key,secret,url,api_user={}):
        '''
            new app using app_dict = {}, id = 0
        '''
        self.url = url
        self.key = key
        self.secret = secret
        if type(api_user)==int:
            self.id = api_user
            self.refresh()
        else:                      
            self.id                  = api_user.get('id','0')                
            self.created             = api_user.get('created','')           
            self.date_of_birth       = api_user.get('date_of_birth','')     
            self.description         = api_user.get('description','')       
            self.device_id           = api_user.get('device_id','')         
            self.email               = api_user.get('email:null','')        
            self.first_name          = api_user.get('first_name','')        
            self.large_image         = api_user.get('large_image','')       
            self.last_name           = api_user.get('last_name','')         
            self.location            = api_user.get('location','')          
            self.medium_image        = api_user.get('medium_image','')      
            self.resource_uri        = api_user.get('resource_uri','')      
            self.sex                 = api_user.get('sex','')               
            self.small_image         = api_user.get('small_image','')       
            self.updated             = api_user.get('updated','')           

    def to_dict(self):
        return self.__dict__
                                
    def refresh(self):
        '''
            update object
        '''
        new_item = self._get('apiuser', self.id)
        self = self.__init__(self.key, self.secret, self.url, new_item) 
 















