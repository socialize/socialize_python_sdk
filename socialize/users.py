from base import ObjectBase , CollectionBase
from datetime import datetime
from simplejson import loads
from django.utils.encoding import smart_str
import math




class ApiUserStats(CollectionBase):
    '''
        Api User Stat is a new endpoint replace api_user, with more information.
        Goal is to replace api_user with api_user_stat.
    '''
    def __init__(self, key,secret,host,app_id):
        self.key = key                                              
        self.secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        params['application'] = self.app_id
        params['application_id'] = self.app_id
        meta, items = self._find('apiuser_stat',params)
        api_user_stats=[]
        for item in items:
            stat = ApiUserStat(self.key, self.secret, self.host,self.app_id, item)
            api_user_stats.append(stat)    
        return meta, api_user_stats
    
    def findOne(self, api_user_id, params={}):
        '''
            This work differently from other endpoints, 
            id in this endpoint refer to stat_id
        '''
        
        params['application'] = self.app_id
        params['application_id'] = self.app_id

        params['user__id'] = api_user_id
        meta, items = self._find('apiuser_stat', params)
        ## RETURN NOTFOUND if user not exist in the application
        try:
            stat = ApiUserStat(self.key, self.secret, self.host,self.app_id,items[0])
        except IndexError:
            raise Exception(404)

        return stat

    def most_active_users(self, params={}):
        params['order_by'] = '-total' 
        return self.find(params)

    def most_recent_users(self, params={}):  
        params['order_by'] = '-id'
        return self.find(params)

    def banned_users(self, params={}):  
        params['is_banned']= 1
        return self.find(params)
        
    def authd_users(self, params={}):
        '''
            NOT YET IMPLEMENTED on partner api
        '''
        pass



class ApiUserStat(ObjectBase):
    '''
        A Single object of API user stats. Support GET only , no update
    '''

    class Device():
        def __repr__(self):
            return '<device id: %s ,username: %s,app_id: %s (%s,%s,%s,%s,%s,%s)>'%(self.id, self.user, self.application,
                    self.country_code, self.device_name, self.language_code,self.platform, self.platform_version, self.sdk_version)
            
        def __init__(self, device={}):
            self.id                  = device.get('id',None)                          
            self.application         = device.get('application',None)     
            self.user                = device.get('user',None)            
            self.user_stat           = device.get('user_stat',None)  
            self.bundle_id           = device.get('bundle_id',None)       

            self.device_udid         = device.get('device_udid',None)     
            self.oauth_token         = device.get('oauth_token',None)     
            
            self.country_code        = device.get('country_code',None)    
            self.device_name         = device.get('device_name',None)     
            self.language_code       = device.get('language_code',None)   
            self.platform            = device.get('platform',None)        
            self.platform_version    = device.get('platform_version',None)
            self.sdk_version         = device.get('sdk_version',None)
            
            
    def __repr__(self):
        return '<api_user id: %s ,username: %s (%s,%s,%s,%s = %s)>'%(self.user.id, self.user.username,
                                self.comments,self.likes, self.views, self.shares,self.total)

    def __init__(self, key,secret,host,app_id, api_user_stat):
        self.host = host
        self.key = key
        self.secret = secret
        self.app_id = app_id
         
        self.id                  = int(api_user_stat.get('id','0'))                
        self.resource_uri        = api_user_stat.get('resource_uri','')
        self.created             = datetime.strptime(api_user_stat.get('created','2001-01-01T00:00:01'), '%Y-%m-%dT%H:%M:%S')           
        self.updated             = datetime.strptime(api_user_stat.get('updated','2001-01-01T00:00:01'), '%Y-%m-%dT%H:%M:%S')           
 
        self.user                = ApiUser(key, secret, host, self.app_id, api_user_stat.get('user',{}))

        self.application         = api_user_stat.get('application','')
        self.comments            = api_user_stat.get('comments',0)
        self.likes               = api_user_stat.get('likes',0)
        self.views               = api_user_stat.get('views',0)
        self.shares              = api_user_stat.get('shares',0)
        self.total               = api_user_stat.get('total',0)
        self.is_banned           = api_user_stat.get('is_banned','')
        
        self.devices             = [self.Device(item) for item in api_user_stat.get('devices',[]) ]
        
        #calculate score
        #self.score               = self.__get_ssz_user_score()
        self.score               = self.__new_ssz_user_score()
        self.mo                  = self.__get_ssz_user_MO()
        self.badges              = self.__get_badges()
    
    def __new_ssz_user_score(self):
        GRAPH_VELOCITY = 2
        
        def activity_score(activity_count, weight):
            return math.log(max(activity_count, 1)*weight)

        def formular(comment, share,like, view):
            # pre defince weight of activity
            weight = { 'like': 20,
                'share': 50,
                'comment':30,
                'view': 5} 
            
            cs = activity_score( comment, weight['comment'])
            ss = activity_score( share, weight['share'])
            ls = activity_score( like, weight['like'])
            vs = activity_score( view, weight['view'])

            return cs+ss+ls+vs

        user_sum = formular( self.comments, self.shares, self.likes, self.views)
        lowest  =  formular( 1,1,1,1)
        highest = formular( 1000,1000,1000,1000)

        return (user_sum - lowest) * (highest * GRAPH_VELOCITY / 100) 
    
    def __get_ssz_user_score(self):
        #totals
        tc = 0 if self.comments < 0 else self.comments
        tl = 0 if self.likes < 0 else self.likes 
        ts = 0 if self.shares < 0 else self.shares  
        tv = 0 if self.views < 0 else self.views     
        #print tc, tl, ts, tv
        
        ##weights
        cw = tc*5.0
        lw = tl*1.3
        sw = ts*9.0
        vw = tv*.03
        #print cw, lw, sw, vw
        
        ##logs
        cl = math.log10(cw+1)
        ll = math.log10(lw+1)
        sl = math.log10(sw+1)
        vl = math.log10(vw+1)
        #print cl, ll, sl, vl
        
        score = (cl+ll+sl+vl)/6.0 * 100.0
        return round(score, 2)
        

    def __get_ssz_user_MO(self):
        #totals
        tc = self.comments
        tl = self.likes
        ts = self.shares
        tv = self.views
        #print tc, tl, ts, tv
        
        #compared ratio
        total = tc+tl+ts
        compared = 0
        if tv > 0:
            compared = (total*1.0)/(tv*1.0)
        #print total, compared
        #give type
        if compared > 0.025:
            return "Contributor"
        return "Voyeur"
    
    def __get_badges(self):
        badges = []
        if self.comments > 30:
            badges.append("commenter")
        if self.likes > 30:
            badges.append("lover")
        return badges
            

    def to_dict(self):
        return self.__dict__

class ApiUsers(CollectionBase):
    '''
        find a list of api users in application
    '''
    def __init__(self, key,secret,host,app_id):
        self.key = key                                              
        self.secret  = secret
        self.host = host
        self.app_id= app_id
        self.next_url = None
        self.previous_url = None        
    
    def find(self, params={}):
        params['application_id'] = self.app_id
        meta, items = self._find('apiuser',params)
        api_users=[]
        for item in items:
            api_user = ApiUser(self.key, self.secret, self.host,self.app_id, item)
            api_users.append(api_user)    
        return meta, api_users
    
    def findOne(self, api_user_id, params={}):
        params['application_id'] = self.app_id
        item = self._findOne('apiuser',api_user_id, params)
        api_user = ApiUser(self.key, self.secret, self.host, self.app_id, item)
        return api_user 

    ## API CANCLE ENDPOINT  will be remove if there 's no complain from website
    #def findBanned(self, params={}):
        #params['application_id'] = self.app_id
        #meta, items = self._find('apiuser',params, verb='banned')
        #api_users=[]
        #for item in items:
            #api_user = ApiUser(self.key, self.secret, self.host,self.app_id, item)
            #api_users.append(api_user)    
        #return meta, api_users
 

class ApiUser(ObjectBase):
    '''
        find a single user from API
        ** API should allow filter by id & application
    '''
    def __repr__(self):
        return '<api_user id: %s ,first_name: %s>'%(self.id, self.first_name)

    def __init__(self, key,secret,host,app_id, api_user):
        '''
            new app using app_dict = {}, id = 0
        '''
        self.host = host
        self.key = key
        self.secret = secret
        self.app_id = app_id
        if type(api_user)==int:
            self.id = api_user
        else:
            self.id                  = int(api_user.get('id','0'))                
            self.resource_uri        = api_user.get('resource_uri','')
            self.created             = datetime.strptime(api_user.get('created','2001-01-01T00:00:01'), '%Y-%m-%dT%H:%M:%S')           
            self.updated             = datetime.strptime(api_user.get('updated','2000-01-01T00:00:01'),'%Y-%m-%dT%H:%M:%S')        

            self.username            = smart_str(api_user.get('username',''), strings_only=True)
            self.date_of_birth       = api_user.get('date_of_birth','')    
            self.description         = api_user.get('description','')       
            self.device_id           = api_user.get('device_id','')         
            self.email               = api_user.get('email','')        
            self.first_name          = api_user.get('first_name','')        
            self.last_name           = api_user.get('last_name','')         
            self.location            = api_user.get('location','')          
            self.sex                 = api_user.get('sex','')               
            self.small_image_uri     = api_user.get('small_image_uri','')       
            self.medium_image_uri    = api_user.get('medium_image_uri','')      
            self.large_image_uri     = api_user.get('large_image_uri','')       
            
            self.stats               = api_user.get('stats','{}')
            self.user_devices        = api_user.get('user_devices','[]') 

    def to_dict(self):
        return self.__dict__
                                
    def refresh(self):
        '''
            update object
        '''
        params = {'application_id': self.app_id}
        new_item = self._get('apiuser',item_id=self.id, params= params)
        self = self.__init__(self.key, self.secret, self.host, self.app_id, new_item) 
    
    def ban(self, app_id):
        '''
            ban current user 
            payload require app_id because api_user_id can be in multiple app with 3rdPartyAuth
            return True when success / else raise Exception
        '''
        payload = {'application_id': app_id}
        return self._post('apiuser',payload=payload, item= self.id, verb='ban')

    def unban(self, app_id):
        '''
            ban current user 
            payload require app_id because api_user_id can be in multiple app with 3rdPartyAuth
            return True when success / else raise Exception
        '''
        payload = {'application_id': app_id}
        return self._post('apiuser',  payload, item=self.id, verb='unban')
    
#    def isbanned(self, app_id):
        #'''
            #check if current user is banned
            #payload require app_id because api_user_id can be in multiple app with 3rdPartyAuth
            #return True when success / else Talse
        #'''
        #payload = {'application_id': app_id, "id":self.id}
        #response = self._get('apiuser',  'banned', payload)
        #if len(response["objects"]) > 0:
            #return True
        #return False
     
        
