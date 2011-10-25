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
    
    def find(self, params={}):
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
        return Application().new()
    
class Application(object):
    def __repr__(self):
        return '<id: %s ,name: %s>'%(self.app_id, self.name)
    
    ## can use kwargs later // 
    def __init__(self,app):
        self.app_id                 = app['id']
        self.android_package_name   = app['android_package_name']
        self.apple_store_id         = app['apple_store_id']
        self.category               = app['category']  
        self.description            = app['description']   
        self.platform               = app['platforms']   
        self.name                   = app['name']  
        self.user_id                = app['user']  

    def new(self):
        self.android_package_name   = ''
        self.apple_store_id         = ''
        self.category               = ''
        self.description            = ''
        self.mobile_platform        = ''   
        self.name                   = ''
        self.user_id                = ''
 
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

    def __construt_response(self,response_header, response_body):
        try:
            status_code = response_header['status']
            
            if status_code[0] != '2':    ## Only accept '2xx'
                raise Exception('Server return status code %i\n%s'%(status_code, content))
        
            content = json.loads(response_body)
            return content
        except Exception, err:
            raise Exception('Bad Response please check url\n%s'%err)

    def get(self,url,params={}):
        response_header, response_body = self.client.request(url,'GET')
        return  self.__construt_response(response_header, response_body)

    def post(key,secret,url,params):
        pass

    def delete(key,secret,url):
        pass

    def put(key,secret, url,params):
        pass


