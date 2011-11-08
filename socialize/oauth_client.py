import httplib2
from oauth2 import *

class OauthClient(httplib2.Http):
    """An oauth client that does things a little more sanely than the bundled one."""
    
    def __init__(self, consumer, token=None, cache=None, timeout=None,
        proxy_info=None):

        if consumer is not None and not isinstance(consumer, Consumer):
            raise ValueError("Invalid consumer.")

        if token is not None and not isinstance(token, Token):
            raise ValueError("Invalid token.")

        self.consumer = consumer
        self.token = token
        self.method = SignatureMethod_HMAC_SHA1()

        httplib2.Http.__init__(self, cache=cache, timeout=timeout, proxy_info=proxy_info)

    def set_signature_method(self, method):
        if not isinstance(method, SignatureMethod):
            raise ValueError("Invalid signature method.")
        self.method = method

    def request(self, uri, method="GET", body='', headers=None,
        redirections=httplib2.DEFAULT_MAX_REDIRECTS, connection_type=None,
        use_oauth_headers=True, parameters=None):
        
        DEFAULT_POST_CONTENT_TYPE = 'application/x-www-form-urlencoded'

        if not isinstance(headers, dict):
            headers = {}

        if method == "POST":
            headers['Content-Type'] = headers.get('Content-Type',
                DEFAULT_POST_CONTENT_TYPE)

        is_form_encoded = \
            headers.get('Content-Type') == 'application/x-www-form-urlencoded'

        if is_form_encoded and body:
            parameters.update(parse_qs(body))

        req = Request.from_consumer_and_token(self.consumer,
            token=self.token, http_method=method, http_url=uri,
            parameters=parameters, body=body, is_form_encoded=is_form_encoded)
        
        req.sign_request(self.method, self.consumer, self.token)

        schema, rest = urllib.splittype(uri)
        if rest.startswith('//'):
            hierpart = '//'
        else:
            hierpart = ''
        host, rest = urllib.splithost(rest)

        realm = schema + ':' + hierpart + host

        if is_form_encoded:
            body = req.to_postdata()

        if not use_oauth_headers:
            uri = req.to_url()
        else:
            headers.update(req.to_header(realm=realm))
            headers['content-Length']=len(body)

        
        print headers
        return httplib2.Http.request(self, uri, method=method, body=body,
            headers=headers, redirections=redirections,
            connection_type=connection_type)

