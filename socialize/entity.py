from django.utils.encoding import smart_str
from base import CollectionBase, ObjectBase
from datetime import datetime
import urllib

class Entities(CollectionBase):
    ''' find() Return collection of Activity

        **  parameter application is required
        **  parameter deleted is to filter not-deleted app.
    '''
    find_valid_constrains = ['format','offset','limit','order_by',
                            'application','entity',]
    findOne_valid_constrains = ['format', 'id'] 
  
    def __init__(self, key,secret,host,app_id):
        self.consumer_key = key                                              
        self.consumer_secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        '''
            return list of entities
        '''
        if self.app_id:
            params['application'] = self.app_id
 
        meta, items = self._find('entity' ,params)
        entities=[]
        for item in items:
            entity = Entity(self.consumer_key, self.consumer_secret, self.host, item)
            entities.append(entity)    
        return meta, entities

    def findOne(self, entity_id, params={}):
        '''
            return single entity object
        '''
        if self.app_id:
            params['application'] = self.app_id

        item = self._findOne('entity',entity_id, params)
        entity = Entity(self.consumer_key, self.consumer_secret, self.host,item)
        return entity                           
        
    def new(self):
        entity =  Entity(self.consumer_key,self.consumer_secret,self.host)
        entity.application = self.app_id
        return entity

    def delete(self, entity_id):

        entity = self.findOne(entity_id)

        if self.app_id == entity.application:
            return entity.delete()
        else:
            raise Exception("can not perform delete for non owner")    
    


class Entity(ObjectBase):
    '''
        Construct entity object
    '''
    def __init__(self, key,secret,host,entity={}):
        self.host = host
        self.consumer_key = key
        self.consumer_secret = secret          
        
        self.created    = datetime.strptime(entity.get('created','2001-01-01T00:00:01'),'%Y-%m-%dT%H:%M:%S')       
        self.application= entity.get('application',None)
        self.resource_uri= entity.get('resource_uri','')
        self.id         = int(entity.get('id','0'))

        #TODO this self.key is over write app's consumer key 
        # I don't think self.key at object level is being use anywhere (only on application) 

        self.key        = entity.get('key','')
        self.original_key= entity.get('original_key','')
        self.name       = smart_str(entity.get('name',''), strings_only=True)   
        self.type       = entity.get('type','') 
        self.views      = entity.get('views',None)       
        self.shares     = entity.get('shares',None)       
        self.likes      = entity.get('likes',None)       
        self.comments   = entity.get('comments',None)
        self.total_activity   = entity.get('total_activity',None)
    
    def __post_payload(self):
        key_encoded = urllib.quote(self.key)
        return {'application_id': self.application,
                'key':key_encoded,
                'name':self.name}

    def __repr__(self):
        return '<id: %s ,key: %s, name: \"%s\" app: %s created: %s>'%(self.id,
                self.key,self.name ,self.application,self.created)   

    def save(self):
        ''' 
            create new entity or update if key exist
        '''
        location = self._post('entity', self.__post_payload())
        self.id =location.split('/')[-2]
        

    def delete(self):
        '''
            delete object
        '''
        if self.id==None or int(self.id) ==0:
            raise Exception('entity_id can not be None or 0')
        return self._delete('entity',self.id) 

    def refresh(self):
        '''
            update object
        '''
        new_item = self._get('entity', self.id)
        self = self.__init__(self.key, self.secret, self.host, new_item) 
 

