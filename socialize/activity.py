from base import CollectionBase, ObjectBase
from users import ApiUsers
from urllib2 import quote
from django.utils.encoding import smart_str
from datetime import datetime
from users import ApiUser
from entity import Entity

class Activities(CollectionBase):
    ''' find() Return collection of Activity

        **  parameter application is required
        **  parameter deleted is to filter not-deleted app.
    '''
    find_valid_constrains = ['format','offset','limit','user', 'user_id','order_by','deleted',
                            'activity_type','application','entity',]
    findOne_valid_constrains = ['format','user', 'id'] ## not allowed any constrain
  
    def __init__(self, key,secret,host,app_id,activity_type):
        self.key = key                                              
        self.secret  = secret
        self.host = host
        self.app_id= app_id
        self.activity_type = activity_type
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        params['application'] = self.app_id
        meta, items = self._find(self.activity_type ,params)
        activities=[]
        for item in items:
            activity = Activity(self.key, self.secret, self.host, item)
            activities.append(activity)    
        return meta, activities
        

class Activity(ObjectBase):
    '''
        Construct activity base on activity_type
        can not create new activity from dashboard
    '''

    def __repr__(self):
        return '<id: %s ,%s %s on \"%s\" in app: %s | %s>'%(self.id,self.user.username,self.activity_type,self.entity.name,self.application, self.created)   

 
    def __init__(self, key,secret,host,activity={}):
        self.host = host
        self.key = key
        self.secret = secret  
        
        self.id                  	= int(activity.get('id','0'))                                                                
        self.resource_uri           = activity.get('resource_uri','')
        self.application   			= activity.get('application',None)     	
        self.activity_type 			= activity.get('activity_type',None)    
        self.created       			= datetime.strptime(activity.get('created','2001-01-01T00:00:01'),'%Y-%m-%dT%H:%M:%S')       

        ## View , Share can't be updated
        self.updated			    = datetime.strptime(activity.get('updated','2001-01-01T00:00:01'),'%Y-%m-%dT%H:%M:%S')                
                                         
        ## Sub-structure
        self.entity                 = Entity(activity.get('entity',{}))
        self.user                   = ApiUser(key, secret, host, self.application, activity.get('user',{}))

        self.lat			        = activity.get('lat',None)             
        self.lng         		  	= activity.get('lng',None)              
        self.share_location			= activity.get('share_location',None)  
        ## View, Like don't have text, and can't be deleted
        self.text          			= activity.get('text',None)      
        self.deleted       			= activity.get('deleted',None)         
        
