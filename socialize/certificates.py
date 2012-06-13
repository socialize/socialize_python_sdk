from base import ObjectBase , CollectionBase
from datetime import datetime
from json import loads

class IphoneCertificate(ObjectBase):
    '''
        find a single iphoien certificate from API
        ** API should allow filter by cert id 
    '''
    def __repr__(self):
        return '<cert id: %s ,code_sign_identity: %s>'%(self.id, self.code_sign_identity)

    def __init__(self, key, secret, host, cert):
        '''
            new cert using app_dict = {}, id = 0
        '''
        self.host = host
        self.consumer_key = key
        self.consumer_secret = secret
        if type(cert)==int:
            self.id = cert
            self.get()
        elif not cert:
            self.id = None
        else:
            self.id                  = int(cert.get('id','0'))                
            self.resource_uri        = cert.get('resource_uri','')
            self.created             = datetime.strptime(cert.get('created',None), '%Y-%m-%dT%H:%M:%S')           
            self.cert_last_updated   = cert.get('cert_last_updated',None)
            self.type                = cert.get('type',None)
            if self.cert_last_updated:
                self.updated         = datetime.strptime(self.cert_last_updated,'%Y-%m-%d')        
            else:
                self.updated         = None
            self.code_sign_identity  = cert.get('code_sign_identity','')    
            self.p12_url             = cert.get('p12_url','')

            self.certificate_expiration_date = datetime.strptime(cert.get('certificate_expiration_date',None), '%Y-%m-%dT%H:%M:%S') 


    def to_dict(self, params={}):
        return self.__dict__
                                
    def get(self):
        '''
            Get available iPhone certificate
        '''
        cert = None
        if self.id:
            params = {'id': self.id}
            cert = self._get('iphone_certificate',item_id=self.id, params= params)
            self.__init__(self.consumer_key, self.consumer_secret, self.host, cert)
        return self
    

     
        
