from django.utils.encoding import smart_str
from base import CollectionBase, ObjectBase
from datetime import datetime

class Entity(ObjectBase):
    '''
        Construct entity object
    '''
    def __init__(self, entity={}):
        self.application= entity.get('application',None)
        self.created    = datetime.strptime(entity.get('created','2001-01-01T00:00:01'),'%Y-%m-%dT%H:%M:%S')       
        self.resource_uri= entity.get('resource_uri','')
        self.id         = int(entity.get('id','0'))
        self.key        = entity.get('key','')
        self.name       = smart_str(entity.get('name',''))   
        self.type       = entity.get('type','') 
        self.views      = entity.get('views',None)       
        self.shares     = entity.get('shares',None)       
        self.likes      = entity.get('likes',None)       
        self.comments   = entity.get('comments',None)      
