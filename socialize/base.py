from hashlib import sha1
from urlparse import urlparse, parse_qs, urlunparse
import urllib
import oauth_client as oauth
import json
import httplib2
import logging

logger = logging.getLogger(__name__)
show_connections = False

class PartnerBase(object):
    base_partner_path = 'partner'
    version = 'v1'
    partner_endpoints = {
            'application'       : 'application',
            'webuser'           : 'web_user',
            'apiuser'           : 'api_user',
            'apiuser_stat'      : 'api_user_stat',
            'iphone_certificate': 'iphone_certificate',
            'view'              : 'view',
            'share'             : 'share',
            'comment'           : 'comment',
            'like'              : 'like',
            'entity'            : 'entity',
            'analytic'          : 'analytic',
            'notification_log'  : 'notification_log',
            }                    

    partner_endpoint_verb = {
            'application' : ['upload_p12','upload_icon', 'notification'],
            'apiuser' : ['ban','unban']
            }

class CollectionBase(PartnerBase):
    def _request(self, endpoint, params={}):
        """
            simple request - response with out parsing any content.
        """
        request_url = '%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint])
 
        request = Request(self.consumer_key,self.consumer_secret)
        response = request.get(request_url, params)
        return response
 
    def _find(self, endpoint, params={}, verb=None):
        """
            Fetches results form the server, optionally based on constraints.
            See the children class for which constraints are supported.
        """
        
        request_url = '%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint])
        if verb:
            if verb in self.partner_endpoint_verb[endpoint]:
                request_url = '%s%s/' % (request_url, verb)
            else:
                raise Exception('%s is not allow in %s endpoint'%(verb, endpoint))
        
        request = Request(self.consumer_key,self.consumer_secret)
        response = request.get(request_url, params)
        meta = response['meta']
        objects = response['objects']
        return meta, objects

    def _findOne(self, endpoint, item_id, params={}):
        """
            Fetches a single result form the server, optionally based on constraints.
            See the children class for which constraints are supported.

            Only ID is supported to find one.
        """ 
        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item_id
                                )
        
        request = Request(self.consumer_key,self.consumer_secret)
        return request.get(request_url, params)

    def _delete(self, endpoint, item):
        '''
            DELETE specific item on api
        '''
        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item
                                )
        request = Request(self.consumer_key,self.consumer_secret)
        return request.delete(request_url)   
                                                     

class ObjectBase(PartnerBase):
    def _post(self, endpoint, payload, item=None, verb=None):
        import vimpdb; vimpdb.set_trace()
        """
            POST payload to api 
            verb is special endpoint for activity
        """
        request_url = '%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint]
                                )

        if item and verb:
            if verb in self.partner_endpoint_verb[endpoint]:
                request_url = '%s%s/%s/' % (request_url,item, verb)
            else:
                raise Error(content='%s is not allow in %s endpoint'%(verb, endpoint))
        request = Request(self.consumer_key,self.consumer_secret)
        if show_connections:
            logger.info(request_url)
        return request.post(request_url, payload)   

    def _put(self, endpoint, payload, item=None, verb=None):
        """
            POST to api with specific id, 
        """

        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item
                                )
        if item and verb:

            if verb in self.partner_endpoint_verb[endpoint]:
                request_url = '%s%s/' % (request_url, verb)
            else:
                raise Error(content='%s is not allow in %s endpoint'%(verb, endpoint)) 
        request = Request(self.consumer_key,self.consumer_secret)
        return request.post(request_url, payload)   

    def _delete(self, endpoint, item_id):
        '''
            DELETE specific item on api
        '''
        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item_id
                                )
        request = Request(self.consumer_key,self.consumer_secret)
        return request.delete(request_url)   

    def _get(self, endpoint, item_id, params={}):
        """
            update itself after post/put
        """
        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item_id
                                )
        
        request = Request(self.consumer_key,self.consumer_secret)
        return request.get(request_url, params=params)   


class Request(object):
    """ client make request
        handle error code here
        return meta, objects
        manage Cache here 
    """
    
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
        self.consumer = oauth.Consumer(key,secret)
        self.token = oauth.Token('','')
        self.client = oauth.Client(self.consumer,self.token)

    def get(self,url,params={}):
        if show_connections:
            logger.info("API Get: %s --%s--" % (url, params))
        url = self.construct_url( url, params)
        response, content = self.client.request(url,'GET')
        return  self.__construct_response(url,response, content,method='GET')

    def post(self,url,payload,params={}):
        if show_connections:
            logger.info("API Post: %s --%s-- ---%s--" % (url, params, payload))
        payload = urllib.quote(json.dumps(payload))
        response, content = self.client.request(url,
                                            method='POST',
                                            body='payload='+payload,)
        return self.__construct_response(url, response, content,payload,method='POST')

    def delete(self,url,payload={}):
        response, content = self.client.request(url,
                                            method='DELETE',
                                            )
        return self.__construct_response(url, response, content,method='DELETE') 
    
    def construct_url(self,url, params={}):
        '''
            reconstruct url using params 
        '''
        #params['format'] = 'json'
        parts = urlparse(url)
        query = parse_qs(parts[4]) or {}
        query.update(params)
        parsed_query = urllib.urlencode([(k, v) for k, vs in query.items() for v in isinstance(vs, list) and vs or [vs]])
        url = urlunparse(
            (parts[0], parts[1], parts[2], parts[3],parsed_query, parts[5])
        )
        return url

    def __construct_response(self, url, response, content, payload='', method=''):
        '''response from request will be json for GET
            POST return url location, and Exception when Fail
            Delete return True else Exception
        '''
        formatted_payload = json.dumps(payload,sort_keys=True, indent=4) 
        status_code = response['status']
        if status_code == '201':
            return response['location']

        elif status_code in ('204','202'):
            return True
        elif status_code =='200':
            try:
                return json.loads(content)
            except Exception, err:
                raise BadResponse(status_code, url, method, payload, "Could not decode content")
        elif status_code =='404':
            raise ErrorNotFound(status_code, url, method, payload,content)
        elif status_code[0] != '2':    ## Only accept '2xx'
            raise Error(status_code, url, method, payload,content)
        return content  


class Error(Exception):
    """
        base clase for exception
    """
    def __init__(self,
            status_code=None,
            url=None,
            method=None,
            payload=None,
            content=None
            ):
        self.status_code = status_code
        self.url = url
        self.method = method
        self.payload = payload
        self.content = content
        if status_code:
            Exception.__init__(self, self.message())
        else:
            Exception.__init__(self, self.content)
    def message(self):
        return "ERROR:\tServer return status code: %s\nurl: %s\nmethod: %s\npayload: %s\ncontent: %s"%(self.status_code, self.url, self.method, self.payload, self.content)

class BadResponse(Error):
    '''
        couldn't decode response.content
    '''
    pass

class ErrorNotFound(Error):
    '''
        status code:404 
        try to access deleted object or not exists
    '''
    pass

class ErrorPermission(Error):
    '''
        status code:403
        or try to delete the object that not belong to user
    '''
    pass

class ErrorMissingParams(Error):
    '''
        missing required parameter
    '''
    pass

class ErrorC2DMwithoutPackageName(Error):
    '''
        missing android package name, 
    '''
