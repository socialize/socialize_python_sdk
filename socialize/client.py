import oauth2 as oauth
import simplejson as json



## Interface
class Partner(object):
    base_partner_path = 'partner'
    version = 'v1'
    partner_endpoints = {
            'application'       : 'application',
            }

    def __init__(self, key, secret, url='http://api.getsocialize.com'):
        self.key= key
        self.secret = secret
        self.url = url

    def applications(self):
        """ return list of applications object"""

        return Applications(self.key,self.secret,self.url)

    def users(app_id):
        """ return user object (not yet implemented)"""
        pass


class CollectionBase(Partner):
    def _find(self, endpoint, params={}):
        """
            Fetches results form the server, optionally based on constraints.
            See the children class for which constraints are supported.
        """

        request_url = '%s/%s/%s/%s/'%(self.url,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint])
        request = Request(self.key,self.secret)
        response = request.get(request_url, params)
        meta = response['meta']
        objects = response['objects']
        return meta, objects

    def _findOne(self, endpoint, app_id, params={}):
        """
            Fetches a single result form the server, optionally based on constraints.
            See the children class for which constraints are supported.

            Only ID is supported to find one.
        """ 
        request_url = '%s/%s/%s/%s/%s/'%(self.url,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                app_id
                                )
        request = Request(self.key,self.secret)
        response= request.get(request_url, params)
        item = response
        return item                                  

    def save(self):
        pass



class Applications(CollectionBase):
    ## next, previous will be carefully implement next release 

    def __init__(self, key,secret,url):
        self.key = key
        self.secret  = secret
        self.url = url
        self.next_url = None
        self.previous_url = None
    
    def find(self):
        meta, items = self._find('application')
        apps = []
        for item in items:
            app = Application(item)
            apps.append(app)
        return meta,apps

    def findOne(self, app_id):
        item = self._findOne('application',app_id)
        app = Application(item)
        return app

    def new(self):
        newapp = {}  ## add blank app
        return Application(newapp)
    

class Application(object):
    def __repr__(self):
        if self.name=="":
            return '<new application>'
        elif self.id==0:
            return '<id: %s, name:%s unsaved app>'%(self.id, self.name) 
        return '<id: %s ,name: %s>'%(self.id, self.name)
       
    def __init__(self,app_dict={}):
        '''
            new app using app_dict = {} > id = 0
        '''
## can't modify
        self.id                         =app_dict.get('id',0) 
        self.created                    =app_dict.get('created','') 
        self.deleted                    =app_dict.get('deleted','') 
        self.last_saved                 =app_dict.get('last_saved','') 
        self.socialize_consumer_key     =app_dict.get('socialize_consumer_key','') 
        self.socialize_consumer_secret  =app_dict.get('socialize_consumer_secret','') 
        self.socialize_app              =app_dict.get('socialize_app','') 

## modifiable  
        self.android_package_name 		=app_dict.get('android_package_name','') 
        self.apple_store_id             =app_dict.get('apple_store_id','') 
        self.category                   =app_dict.get('category','') 
        self.description                =app_dict.get('description','') 
        self.name                       =app_dict.get('name','') 
        self.platforms                  =app_dict.get('platforms',[]) 
        self.resource_uri               =app_dict.get('resource_uri','') 
        self.stats                      =app_dict.get('stats','') 
        self.user                       =app_dict.get('user','') 

    def save():
        
        
        return True
    

    def to_dict(self):
        return self.__dict__

class Request(object):
    """ client make request
        handle error code here
        
        return meta, objects

    """


    partner_endpoints = {
            'application':'application',
            }

    
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
        self.consumer = oauth.Consumer(key,secret)
        self.token = oauth.Token('','')
        self.client = oauth.Client(self.consumer,self.token)

    def __construt_response(self, url, response_header, response_body):
        ## response from request will be json.
        
        try:
            status_code = response_header['status']
            content = json.loads(response_body)

            if status_code[0] != '2':    ## Only accept '2xx'
                raise Exception('Server return status code %i\n%s'%(status_code, content))
            return content
        except Exception, err:
            raise Exception('Bad Response please check url:%s\n%s'%(url,err))

    def get(self,url,params={}):
        response_header, response_body = self.client.request(url,'GET')
        return  self.__construt_response(url,response_header, response_body)

    def post(key,secret,url,payload):
        response_header, response_body = self.client.request(url,
                                            method='POST',
                                            body='payload='+json.dumps(payload))
        print response_header
        print response_body

    def delete(key,secret,url):
        pass

    def put(key,secret, url,params):
        pass


