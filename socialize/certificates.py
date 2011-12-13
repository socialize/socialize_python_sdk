from base import ObjectBase , CollectionBase
from datetime import datetime
from simplejson import loads

class IphoneCertificate(ObjectBase):
    '''
        find a single iphoien certificate from API
        ** API should allow filter by cert id 
    '''
    def __repr__(self):
        return '<cert id: %s ,code_sign_identity: %s>'%(self.id, self.code_sign_identity)

    def __init__(self, key, secret, host, app_id, cert):
        '''
            new cert using app_dict = {}, id = 0
        '''
        self.host = host
        self.key = key
        self.secret = secret
        self.app_id = app_id
        if type(cert)==int:
            self.id = cert
        else:
            self.id                  = int(cert.get('id','0'))                
            self.resource_uri        = cert.get('resource_uri','')
            self.created             = datetime.strptime(cert.get('created',None), '%Y-%m-%dT%H:%M:%S')           
            self.updated             = datetime.strptime(cert.get('cert_last_updated',None),'%Y-%m-%dT%H:%M:%S')        

            self.code_sign_identity       = cert.get('date_of_birth','')    
                


    def to_dict(self, params={}):
        return self.__dict__
                                
    def get(self):
        '''
            Get available iPhone certificate
        '''
        params = {'id': self.id}
        cert = self._get('iphone_certificate',item_id=self.id, params= params)
        return cert
    
    def refresh(self):
        '''
            update object
        '''
        params = {'id': self.id}
        new_item = self._get('iphone_certificate',item_id=self.id, params= params)
        self = self.__init__(self.key, self.secret, self.host, self.app_id, new_item) 

     
        
