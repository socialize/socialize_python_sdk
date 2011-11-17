
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
    
    def upload_icon(self, base64_img):
        '''
            upload base64 encoded image for app_icon
            return True when success else raise exception
        '''
        payload = {'icon_base64': base64_img}
        resp = self._post( endpoint = 'application',
                payload = payload,
                item=self.id,
                verb='upload_icon')
        return resp

    def upload_p12(self, p12_base64, key_password):
        '''
            upload base64 encoded p12 for notification system
            return True when success else raise exception
        '''
        payload = {'key_password': key_password,
                'p12_base64': p12_base64}

        resp= self._post(endpoint= 'application', payload=payload, item=self.id,verb='upload_p12')
        return resp  
