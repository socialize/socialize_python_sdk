from django.utils.encoding import smart_str
from base import CollectionBase, ObjectBase
from datetime import datetime

class Entities(CollectionBase):
    ''' find() Return collection of Activity

        **  parameter application is required
        **  parameter deleted is to filter not-deleted app.
    '''
    find_valid_constrains = ['format','offset','limit','order_by',
                            'application','entity',]
    findOne_valid_constrains = ['format', 'id'] 
  
    def __init__(self, key,secret,host,app_id):
        self.key = key                                              
        self.secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        '''
            return list of entities
        '''
        params['application'] = self.app_id
        meta, items = self._find('entity' ,params)
        entities=[]
        for item in items:
            entity = Entity(self.key, self.secret, self.host, item)
            entities.append(entity)    
        return meta, entities

    def findOne(self, entity_id, params={}):
        '''
            return single entity object
        '''
        params['application_id'] = self.app_id
        item = self._findOne('entity',entity_id, params)
        entity = Entity(self.key, self.secret, self.host,item)
        return entity                           
                                  
class Entity(ObjectBase):
    '''
        Construct entity object
    '''
    def __init__(self, key,secret,host,entity={}):
        self.host = host
        self.key = key
        self.secret = secret          
        
        self.created    = datetime.strptime(entity.get('created','2001-01-01T00:00:01'),'%Y-%m-%dT%H:%M:%S')       
        self.application= entity.get('application',None)
        self.resource_uri= entity.get('resource_uri','')
        self.id         = int(entity.get('id','0'))

        self.key        = entity.get('key','')
        self.name       = smart_str(entity.get('name',''))   
        self.type       = entity.get('type','') 
        self.views      = entity.get('views',None)       
        self.shares     = entity.get('shares',None)       
        self.likes      = entity.get('likes',None)       
        self.comments   = entity.get('comments',None)
        self.total_activity   = entity.get('total_activity',None)

    def __repr__(self):
        return '<id: %s ,key: %s, name: \"%s\" app: %s created: %s>'%(self.id,
                self.key,self.name ,self.application,self.created)   

    