
from base import CollectionBase, ObjectBase, ErrorC2DMwithoutPackageName
from users import ApiUsers
from certificates import IphoneCertificate
from urllib2 import quote
from notifications import NotificationLogs
from utils import smart_str
import logging
logger = logging.getLogger(__name__)

class Applications(CollectionBase):
    ''' find() Return collection of Application
        findOne(id) Return single application by id 

        **  parameter user is required
        **  parameter deleted is to filter not-deleted app.
    '''
    ## next, previous will be carefully implement next release 
    find_valid_constrains = ['format','offset','limit','user',
                'user_id','order_by','deleted','is_socialize_editable']
    findOne_valid_constrains = ['format','user', 'user_id'] ## not allowed any constrain

    def verify_constrain(self,params,is_findOne):
        for query in params:
            if is_findOne:
                if query not in self.findOne_valid_constrains:
                    raise Exception("parameter %s is not acceptable in findOne()\n %s"%(query, self.findOne_valid_constrains))
            else:
                if query not in self.find_valid_constrains:
                    raise Exception("parameter %s is not acceptable in find()\n %s"%(query, self.find_valid_constrains))
                            
    def __init__(self, key,secret,host,user=None,socialize_consumer_key=None):
        self.consumer_key = key                                              
        self.consumer_secret  = secret
        self.host = host
        self.user= user
        self.socialize_consumer_key= socialize_consumer_key
        self.next_url = None
        self.previous_url = None
    
    def find(self,params={}):
        params['user_id']=self.user
        params['user']=self.user #for api changes, make sure both work
        self.verify_constrain(params, is_findOne=False)
        meta, items = self._find('application',params)
        apps = []
        for item in items:
            app = Application(self.consumer_key,self.consumer_secret,self.host,item)
            apps.append(app)
        return meta,apps

    def filter_by_id(self,ids=[]):

        meta, items = self._find('application',{"id__in":ids})
        
        apps=[]
        for item in items:
            app = Application(self.consumer_key,self.consumer_secret,self.host,item)
            apps.append(app)
        return meta,apps
 

    def findOne(self, app_id, params={}):
        params['user_id'] = self.user
        params['user']=self.user #for api changes, make sure both work
        self.verify_constrain(params, is_findOne=True)
        item = self._findOne('application',app_id,params)
        app = Application(self.consumer_key,self.consumer_secret,self.host,item)
        return app

    def findByKey(self, params={}):
        if self.socialize_consumer_key:
            params['socialize_consumer_key']=self.socialize_consumer_key
        else:
            raise Exception("socialize_consumer_key is invalid")
        
        meta, items = self._find('application',params)
        try:
            app = Application(self.consumer_key,self.consumer_secret,self.host,items[0])
            return app
        except IndexError:
            raise Exception(404)
 
    def findAllSocialize(self, params={}, is_socialize=True):
        params['is_socialize_editable'] = is_socialize
        meta, items = self._find('application',params)
        apps = []
        for item in items:
            app = Application(self.consumer_key,self.consumer_secret,self.host,item)
            apps.append(app)
        return meta,apps

    def new(self):
        return Application(self.consumer_key,self.consumer_secret,self.host)

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
        self.consumer_key = key
        self.consumer_secret = secret  

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
            self.push_certificate           =app.get('push_certificate', None)
            self.is_socialize_editable      =app.get('is_socialize_editable', True)
            self.c2dm_token_source          =app.get('c2dm_token_source', 'socialize')

            self.custom_propagation_domain  =app.get('custom_propagation_domain', None)
            
            self.twitter_consumer_key       =app.get('twitter_consumer_key', None)
            self.twitter_consumer_secret       =app.get('twitter_consumer_secret', None)
            
            self.notification_quotas        =app.get('quotas', {})
            self.__update_notification_quotas()
            
            
            ## modifiable  
            notifications_enabled           =app.get('notifications_enabled', False)
            if type(notifications_enabled) == str:
                if notifications_enabled == "false":
                    notifications_enabled = False
                else:
                    notifications_enabled = True
            self.notifications_enabled      =notifications_enabled
 
            self.android_package_name 	    =app.get('android_package_name','') 
            self.c2dm_sender_auth_token     =app.get('c2dm_sender_auth_token','')
            self.apple_store_id             =app.get('apple_store_id','') 
            self.category                   =app.get('category','') 
            self.description                =smart_str(app.get('description',''), strings_only=True)
            self.name                       =smart_str(app.get('name',''), strings_only=True) 
            self.mobile_platform            =app.get('platforms',[]) 
            self.resource_uri               =app.get('resource_uri','') 
            self.stats                      =app.get('stats','') 
            self.display_name               =self.name
            self.icon_url                   =app.get('icon_url',None)
            
            self.stats                      =app.get('stats',{})
            
            if len(self.stats) > 0:
                self.__calculate_stats(self.stats )
            #logger.info(self.stats)
            
            #to make forward and backward compatible with API-user changes (temporary)
            user_id = int(app.get('user','0'))
            if user_id == 0:
                user_id = int(app.get('user_id','0'))
            self.user  			    =user_id

    
    def __update_notification_quotas(self):
        #update quota logic that is a bit messy from server
        quotas = self.notification_quotas
        if "android" in quotas:
            quotas["android"]["quota_reached"] = False
            quotas["android"]["quota_reached_type"] = ""
            if "android" in quotas:
                if quotas["android"]["quota_used"] >= quotas["android"]["quota_limit"]:
                    quotas["android"]["quota_reached"] = True
                    quotas["android"]["quota_reached_type"] = "socialize"
                if quotas["android"]["quota_used"] == 1 and self.c2dm_token_source != "socialize":
                    quotas["android"]["quota_reached"] = True
                    quotas["android"]["quota_reached_type"] = "google"
            self.notification_quotas = quotas
            
    
    #math helpers for end user
    def __calculate_stats(self, stats):
        #get views per user
        #get actions per user
        if "users" in stats:
            
            if "views" in stats:
                views = stats.get("views", 0) * 1.0

                if "unique_devices" in stats:
                    users = stats.get("unique_devices", 0) * 1.0
                else:
                    users = stats.get("users", 0) * 1.0

                if users <= 0:
                    stats["views_per_user"] = 0
                else:
                    stats["views_per_user"] = round(views/users, 2) 
            if "comments" in stats and "likes" in stats and "shares" in stats:
                stats["actions_per_user"] = None
                comments = stats.get("comments", 0)
                likes = stats.get("likes", 0)
                shares = stats.get("shares", 0)
                actions = 0.0
                try: 
                    actions = (comments + likes + shares) * 1.0
                except:
                    pass
                if users <= 0:
                    stats["actions_per_user"] = 0
                else:
                    stats["actions_per_user"] = round(actions/users, 2)
    def validate_c2dm_token(self):
        if self.c2dm_sender_auth_token and not self.android_package_name:
            raise ErrorC2DMwithoutPackageName(status_code=400, content="Need android package name in order to send smart alert")
                
    

    def __to_post_payload(self,isPost=True):    
        ## PARTNER api model accept only 50 char_len
        self.name = self.name[:49]
        
        if isPost:
            ## POST
            item ={    "category" : self.category,
                        "description" : self.description,
                        "mobile_platform" : self.mobile_platform,
                        "name" : self.name,
                        "user_id" : self.user,
                        'android_package_name'   :self.android_package_name,  
                        'c2dm_sender_auth_token' :self.c2dm_sender_auth_token,
                        'apple_store_id'         :self.apple_store_id,
                        "icon_url"               :self.icon_url,
                        "twitter_consumer_key"   :self.twitter_consumer_key,
                        "twitter_consumer_secret":self.twitter_consumer_secret,
                        "custom_propagation_domain" :self.custom_propagation_domain

                     }

        else:
            ## update function using POST http method
            item ={
                        'android_package_name'      :self.android_package_name,  
                        'apple_store_id'            :self.apple_store_id,        
                        'category'                  :self.category,              
                        'description'               :self.description,           
                        'name'                      :self.name,                  
                        'mobile_platform'           :self.mobile_platform,       
                        'resource_uri'              :self.resource_uri,          
                        'stats'                     :self.stats,                 
                        'user'                      :self.user,
                        'deleted'                   :self.deleted,
                        'icon_url'                  :self.icon_url,
                        "twitter_consumer_key"      :self.twitter_consumer_key,
                        "twitter_consumer_secret"   :self.twitter_consumer_secret,
                        "custom_propagation_domain" :self.custom_propagation_domain
                    }
        return item

    def refresh(self):
        '''
            update object
        '''
        new_item = self._get('application', self.id)
        self = self.__init__(self.consumer_key, self.consumer_secret, self.host, new_item) 

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
            self._put('application', self.__to_post_payload(False), self.id)
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
        api_users = ApiUsers(self.consumer_key,self.consumer_secret,self.host,self.id)
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

        resp= self._post(endpoint= 'application',
                payload=payload,
                item=self.id,
                verb='upload_p12')
        return resp
    
    def get_iphone_certificate(self,params={}):
        '''
            Get available iPhone certificate
        '''
        iphone_cert = IphoneCertificate(self.consumer_key, self.consumer_secret, self.host, self.push_certificate)
        cert = iphone_cert.get()
        return cert
    
    def get_notification_logs(self,params={}):
        '''
            Get available notification logs
        '''
        notification_logs = NotificationLogs(self.consumer_key, self.consumer_secret, self.host, self.id)
        meta, logs = notification_logs.find(params)
        return logs
        
    def set_notifications_enabled(self, enabled):
        '''
            set notifications enabled to True or False
            return True when success else raise exception
        '''
        payload = {'notifications_enabled': enabled }
        resp = self._put( endpoint = 'application',
                payload = payload,
                item=self.id)
        return resp
    
    def set_c2dm_token(self, token):
        '''
            set C2DM Token
        '''
        self.validate_c2dm_token()
        payload = {'c2dm_sender_auth_token': token, 'android_package_name': self.android_package_name }
        resp = self._put( endpoint = 'application',
                payload = payload,
                item=self.id)
        return resp

    def send_notification(self, message, user_id_list=None, url=None, device_list=None, entity_id=None, subscription=None, broadcast_user_set=None):
        '''
            set notifications enabled to True or False
            return True when success else raise exception
            users must be a list of integer
            subscription type [optional] by default is "developer_notification"
        '''
        payload = {'message': message}
        
        if broadcast_user_set:
            payload.update({"broadcast_user_set" : broadcast_user_set})
             
        if type(user_id_list)==list:
            user_id_list = [ int(u) for u in user_id_list ]
            payload.update({ "users": user_id_list })
        if url:
            payload.update({ "url": url })
        if device_list:
            payload.update({ "devices": device_list })
        if entity_id:
            payload.update({ "entity_id": entity_id })
        if subscription:
            payload.update({ "subscription": subscription})
        if url:
            payload.update({"url":url})
        
        resp= self._post(endpoint= 'application',
                payload=payload,
                item=self.id,
                verb='notification')
        return resp

    def android_market_url(self,  is_mobile=False):
#        if is_mobile:
#            return  "market://apps/android?p=%s" % self.android_package_name
        return "http://play.google.com/store/apps/details?id=%s" % self.android_package_name  

    def appstore_url(self):
        return "http://itunes.apple.com/us/app/id%s" % self.apple_store_id      

    def amazon_android_market_url(self,  is_mobile=False):
#        if is_mobile:
#            return  "amzn://apps/android?p=%s" % self.android_package_name
        return "http://www.amazon.com/gp/mas/dl/android?p=%s" % self.android_package_name
