from urlparse import urlparse, parse_qs, urlunparse
import urllib
import oauth2 as oauth
import simplejson as json
import httplib2

class PartnerBase(object):
    base_partner_path = 'partner'
    version = 'v1'
    partner_endpoints = {
            'application'       : 'application',
            'webuser'           : 'web_user',
            'apiuser'           : 'api_user',
            }                    

    partner_endpoint_verb = {
            'application' : ['upload_p12','upload_icon'],
            'apiuser' : ['ban']
            }

class CollectionBase(PartnerBase):
    def _find(self, endpoint, params={}):
        """
            Fetches results form the server, optionally based on constraints.
            See the children class for which constraints are supported.
        """
        
        request_url = '%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint])
        request = Request(self.key,self.secret)
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
        request = Request(self.key,self.secret)
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
        request = Request(self.key,self.secret)
        return request.delete(request_url)   
                                                     

class ObjectBase(PartnerBase):
    def _post(self, endpoint, payload, item=None, verb=None):
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
                raise Exception('%s is not allow in %s endpoint'%(verb, endpoint))
        request = Request(self.key,self.secret)
        return request.post(request_url, payload)   

    def _put(self, endpoint, item_id, payload, verb=None):
        """
            PUT payload to specific item_id on api
            item_id can be <id>/verb/

        """

        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item_id
                                )
        if verb:
            if verb in self.partner_endpoint_verb[endpoint]:
                request_url = '%s%s/' % (request_url, verb)
            else:
                raise Exception('%s is not allow in %s endpoint'%(verb, endpoint)) 
        request = Request(self.key,self.secret)
        return request.put(request_url, payload)   

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
        request = Request(self.key,self.secret)
        return request.delete(request_url)   

    def _get(self, endpoint, item_id):
        """
            update itself after post/put
        """
        request_url = '%s/%s/%s/%s/%s/'%(self.host,
                                self.base_partner_path,
                                self.version,
                                self.partner_endpoints[endpoint],
                                item_id
                                )
        request = Request(self.key,self.secret)
        return request.get(request_url, params={})   


class Request(object):
    """ client make request
        handle error code here
        return meta, objects

    """
    
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret
        self.consumer = oauth.Consumer(key,secret)
        self.token = oauth.Token('','')
        self.client = oauth.Client(self.consumer,self.token)

    def get(self,url,params={}):
        
        url = self.construct_url( url, params)
        response, content = self.client.request(url,'GET')
        return  self.__construct_response(url,response, content)

    def post(self,url,payload,params={}):
        payload = json.dumps(payload)
        response, content = self.client.request(url,
                                            method='POST',
                                            body='payload='+payload)
        print '#' *100
        print payload
        print '#' * 20 , 'before txn'
        return self.__construct_response(url, response, content,payload)
    
    def put(self, url,payload):
        '''
            HACKED oauth2 doesn't like PUT method, so I need to modify it. in the parameters.
        '''
        url_payload = urllib.quote(json.dumps(payload))
        url += '?payload=%s'%url_payload
        req = oauth.Request.from_consumer_and_token(self.consumer, 
                    token=self.token, http_method='PUT', http_url=url, 
                    )

        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        headers =  req.to_header()
        headers['content-length']= '0'

        http =  httplib2.Http()
        response, content  = http.request(url, method='PUT',headers=headers )
        return self.__construct_response(url, response, content)

    def delete(self,url):
        response, content = self.client.request(url,
                                            method='DELETE',
                                            )
        return self.__construct_response(url, response, content) 
    
    def construct_url(self,url, params={}):
        '''
            reconstruct url using params 
        '''
        params['format'] = 'json'
        parts = urlparse(url)
        query = parse_qs(parts[4]) or {}
        query.update(params)
        url = urlunparse(
            (parts[0], parts[1], parts[2], parts[3], urllib.urlencode(query), parts[5])
        )
        return url

    def __construct_response(self, url, response, content, payload=''):
        '''response from request will be json for GET
            POST/PUT return url location, and Exception when Fail
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
                raise Exception('Bad response please check\n%s\n%s\n%s'%(url, formatted_payload, err))
        elif status_code[0] != '2':    ## Only accept '2xx'
            raise Exception('Server return status code %s\n%s\n%s\n%s'%(status_code,formatted_payload,url,content))
        return content      
