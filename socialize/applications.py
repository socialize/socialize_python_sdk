
from base import CollectionBase, ObjectBase
from users import ApiUsers

class Applications(CollectionBase):
    ''' find() Return collection of Application
        findOne(id) Return single application by id 

        **  parameter user is required
        **  parameter deleted is to filter not-deleted app.
    '''
    ## next, previous will be carefully implement next release 
    find_valid_constrains = ['format','offset','limit','user','order_by','deleted']
    findOne_valid_constrains = ['format','user'] ## not allowed any constrain

    def verify_constrain(self,params,is_findOne):
        for query in params:
            if is_findOne:
                if query not in self.findOne_valid_constrains:
                    raise Exception("parameter %s is not acceptable in findOne()\n %s"%(query, self.findOne_valid_constrains))
            else:
                if query not in self.find_valid_constrains:
                    raise Exception("parameter %s is not acceptable in find()\n %s"%(query, self.find_valid_constrains))
                            
    def __init__(self, key,secret,host,user):
        self.key = key                                              
        self.secret  = secret
        self.host = host
        self.user= user
        self.next_url = None
        self.previous_url = None
    
    def find(self,params={}):
        params['user']=self.user
        self.verify_constrain(params, is_findOne=False)
        meta, items = self._find('application',params)
        apps = []
        for item in items:
            app = Application(self.key,self.secret,self.host,item)
            apps.append(app)
        return meta,apps

    def findOne(self, app_id, params={}):
        params['user'] = self.user
        self.verify_constrain(params, is_findOne=True)
        item = self._findOne('application',app_id,params)
        app = Application(self.key,self.secret,self.host,item)
        return app

    def new(self):
        return Application(self.key,self.secret,self.host)

    def delete(self, app_id):
        '''
            verify app owner by using findOne() 
            return True/ False
        '''
        app = self.findOne(app_id)

        if self.user == app.user:
            return app.delete()
        else:
            raise Exception("can not perform delete for non owner")

class Application(ObjectBase):
    def __repr__(self):
        if self.name=="":
            return '<new application>'
        elif self.id==0:
            return '<id: %s, name:%s unsaved app>'%(self.id, self.name) 
        return '<id: %s ,name: %s>'%(self.id, self.name)
       
    def __init__(self, key,secret,host,app={}):
        ''' if app = int return app(id)
            elif app = {} init app with dict
            new app using app = {}, id = 0
        '''
        self.host = host
        self.key = key
        self.secret = secret  

        if type(app)==int:
            self.id = app
            self.refresh()
        else:
            ## can't modify
            self.id                         =int(app.get('id',0)) 
            self.created                    =app.get('created','') 
            self.deleted                    =app.get('deleted','') 
            self.last_saved                 =app.get('last_saved','') 
            self.socialize_consumer_key     =app.get('socialize_consumer_key','') 
            self.socialize_consumer_secret  =app.get('socialize_consumer_secret','') 
            self.socialize_app              =app.get('socialize_app','') 

            ## modifiable  
            self.android_package_name 		=app.get('android_package_name','') 
            self.apple_store_id             =app.get('apple_store_id','') 
            self.category                   =app.get('category','') 
            self.description                =app.get('description','') 
            self.name                       =app.get('name','') 
            self.mobile_platform            =app.get('platforms',[]) 
            self.resource_uri               =app.get('resource_uri','') 
            self.stats                      =app.get('stats','') 
            self.user                       =int(app.get('user','0'))
            self.display_name               =self.name
            self.icon_url                   =app.get('icon_url',None)

    def __to_post_payload(self,isPost=True):    
        '''
            isPost = Add new application
            not isPost = PUT , update application
        '''
## PARTNER api model accept only 50 char_len
        self.name = self.name[:49]

        if isPost:
            ## POST
            item ={    "category" : self.category,
                        "description" : self.description,
                        "mobile_platform" : self.mobile_platform,
                        "name" : self.name,
                        "user_id" : self.user
                    }
        else:
            ##PUT
            item ={
                        'android_package_name'   :self.android_package_name,  
                        'apple_store_id'         :self.apple_store_id,        
                        'category'               :self.category,              
                        'description'            :self.description,           
                        'name'                   :self.name,                  
                        'mobile_platform'        :self.mobile_platform,       
                        'resource_uri'           :self.resource_uri,          
                        'stats'                  :self.stats,                 
                        'user'                   :self.user,
                        'deleted'                :self.deleted,
                    }
        return item

    def refresh(self):
        '''
            update object
        '''
        new_item = self._get('application', self.id)
        self = self.__init__(self.key, self.secret, self.host, new_item) 

    def save(self):
        '''
            handle post & put for application
        '''
        if int(self.user) ==0:
            raise Exception("Unable to create or update with user=0")

        if int(self.id)==0: #POST
            location = self._post('application', self.__to_post_payload(True))
            self.id =location.split('/')[-2]
        else:           #PUT
            self._put('application', self.id, self.__to_post_payload(False))
        #self.refresh()
        
    def delete(self):
        '''
            Delete application
            Note: you can either delete from Applications or Application
        '''
        if int(self.user)== 0 or int(self.id)== 0:
            raise Exception("Unable to delete with app_id or user is 0")
        
        return self._delete('application',self.id)
    
    def to_dict(self):
        return self.__dict__

    def list_api_users(self,params={}):
        '''
            list all available users in the application
        '''
        api_users = ApiUsers(self.key,self.secret,self.host,self.id)
        collection = api_users.find(params)
        return collection

    def upload_p12(self, p12_base64, key_password):
        '''
            upload base64 encoded p12 for notification system
            return True when success else raise exception
        '''
        payload = {'key_password': key_password,
                'p12_base64': p12_base64}

        payload = {"key_password":"success", "p12_base64":"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"}

        resp= self._post(endpoint= 'application', payload=payload, item=self.id,verb='upload_p12')
        return resp  
