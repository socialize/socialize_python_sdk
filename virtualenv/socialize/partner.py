import oauth2 as oauth
import simplejson as json
## REQUEST ##
from client import Request,Applications, Partner
from client import Application
from urlparse import parse_qs
import random

'''
    local
'''
#url = 'http://127.0.0.1:8000'
#key = '6118f9f1-a8a2-45c4-aefa-226a6d5b4755'
#secret = 'c1270fbd-4ae2-49f7-b16e-bc447cf463c9'
#qa_id  = 130827

'''
    stage
'''
url = 'http://stage.api.getsocialize.com'
key= '1878ed35-6d08-410c-a441-ba21d754ec36' 
secret = 'cf3cb3d5-6e90-4fd2-a8e7-8a05c028e18a'  
qa_id = 145874

payload = {
    "category" : 'what ever',
    "description" : 'some thing else',
    "mobile_platform" : ["iPhone", "android", "WM7", "QT"],
    "name" : 'super awesome app',
    "user_id" : qa_id
    }  

def testOauthGet():
    '''
        this test use standard oauth connect to api
        
        response: { status_code, ... }
        content: 
            {   'meta':{ ... },
                'objects':[{...}, ]
            }
    '''
    url = 'http://stage.api.getsocialize.com/partner/v1/application/?format=json&limit=3'
    method = 'GET'
    consumer = oauth.Consumer(key,secret)
    token = oauth.Token('','')

    client = oauth.Client(consumer,token)
#resp,content = client.request(url, 'GET',parameters='{format:json}',use_oauth_headers=True)
    resp , content = client.request(url, method)
    print '*'*150
    for i in resp:
        print i, resp[i]
    print '*'*150
    content = json.loads(content)
    for i in content:
        print content[i]  

def testClientGet():
    '''
        this test using Request class 
        Request().get(url)
        
        this class handle low-level http request, response code
        allow only status code = 200
        return content:
            { meta: { ... },
              objects': [ {...}, ]
            }
        
    '''
    url = 'http://stage.api.getsocialize.com/partner/v1/application/?format=json'

    request = Request(key,secret)
    content= request.get(url)
    print content

def testApplicationFind():
    '''
       this test using Applications.find()
       return list of Application object:
            [ <Application> ... ]
    '''

    apps = Applications(key, secret , url)
    result = apps.find()
    for a in result:
        print a

def testApplicationFindOne():
    '''
        this test using Applications.findOne()
        return Application object:
            <Application>

    '''
    apps = Applications(key,secret,url)
    result = apps.findOne(42)
    print result.to_dict()

def testPartnerGetApp():
    '''
        Partner.applications.find()
    '''
    partner = Partner(key,secret,url)
    apps = partner.applications()
    meta, result = apps.find()
    print '*' * 150
    print meta
    for m in meta:
        print '\t',m ,':',meta[m]

    print '*' * 150
    print result

def testPartnerCreateApp():
    partner = Partner(key,secret,url)
    applications = partner.applications()
    app =  applications.new()
    print app

    print app.to_dict()
    app.name = '123'
    print app


def testOauthPost():
    url = 'http://stage.api.getsocialize.com/partner/v1/application/'
    method = 'POST'
    consumer = oauth.Consumer(key,secret)
    token = oauth.Token('','')

    client = oauth.Client(consumer,token)
#resp,content = client.request(url, 'GET',parameters='{format:json}',use_oauth_headers=True)

    resp , content = client.request(url, method, body='payload='+json.dumps(payload))
    print '*'*150
    for i in resp:
        print i, resp[i]
    print '*'*150
           
def testRequestPost():
    url = 'http://stage.api.getsocialize.com/partner/v1/application/'
    request = Request(key,secret)
    location = request.post(url, payload)
    print location  


def testPartnerSaveApp():
    partner = Partner(key,secret,url)
    app = partner.application()
    app.name = 'testApp'
    app.category = 'test category'
    app.mobile_platform = ['iPhone']
    app.user = qa_id
    app.save()
    print app.__dict__


def testRequestPut():
    url = 'http://stage.api.getsocialize.com/partner/v1/application/323080/'
    request = Request(key,secret)
    request.put(url, payload)

def testPartnerUpdateApp():
    partner = Partner(key,secret,url)
    apps = partner.applications()
    
    
    #app_id = 299932  ## local
    app_id = 323088  ## stage
    app = apps.findOne(app_id)
    print app
    
    app.name
    app.name = str(random.random())
    app.category = 'test category'
    app.mobile_platform = ['iPhone']
    app.user = qa_id
    app.description = 'abc'

    print '&' *0
    
    print '&' * 20
    
    print '&' * 20


    app.save()  ##PUT
    print '*' * 20
    print app.name 
    app.refresh()
    print app.name
    app.name = str(random.random())
    app.save()  ##PUT
    print app.name    

def testConstructUrl():
    url = 'http://stage.api.getsocialize.com/partner/v1/application/'
    params = {'user':qa_id, 'format':'json'}
    request = Request(key,secret)
    print request.construct_url(url,params)


def testFindByUser():
    partner = Partner(key,secret,url)
    apps = partner.applications()
    params = {'user':qa_id}
    result = apps.find(params)
    for i in result:
        print i

def testAll():           
    testOauthGet() 
    testClientGet()
    testApplicationFind()
    testApplicationFindOne()
    testPartnerGetApp()
    testPartnerCreateApp()
    testOauthPost()
    testRequestPost()
    testPartnerSaveApp()
    testRequestPut()
    
    testPartnerUpdateApp()
    testFindByUser()
    testConstructUrl()

#testAll()
#testApplicationFindOne()
#testPartnerSaveApp()
#testRequestPut()
#testPartnerSaveApp()
testPartnerUpdateApp()
