from applications import Applications , Application
from users import ApiUser
class Partner(object):

    def __init__(self, key, secret, host='http://api.getsocialize.com', ):
        self.key= key
        self.secret = secret
        self.host = host
        

    def applications(self,user):
        """ return collection of applications object"""
        return Applications(self.key,self.secret,self.host,user)

    def application(self,app={}):
        """ 
            return new application object or application object
            if typ(app) == int return app from api
                type(app) == dict return Application base on value in dict
                dict = {} return new app
        """
        return Application(self.key,self.secret,self.host,app)

    def api_user(self,api_user_id):
        """ return api user object"""
        return ApiUser(self.key,self.secret,self.host,api_user_id)   


