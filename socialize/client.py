from applications import Applications , Application
from users import ApiUser , ApiUsers, ApiUserStats, ApiUserStat
from activity import Activities
from entity import Entities
from analytic import Analytics

class Partner(object):
    '''
        Interface for Partner API
    '''
    def __init__(self, key, secret, host='http://api.getsocialize.com', ):
        self.key= key
        self.secret = secret
        self.host = host

    def analytics(self, app_id):
        return Analytics(self.key, self.secret, self.host, app_id)

    def applications(self,user=None, socialize_consumer_key=None):
        """ return collection of applications object
            create new app* applications.new()
            list apps* applications.find()  / findOne(app_id)
        """
        if user:
            return Applications(self.key,self.secret,self.host,
                    user,
                    socialize_consumer_key=None)
        else:
            return Applications(self.key,self.secret,self.host,
                    user=None,
                    socialize_consumer_key=socialize_consumer_key)


    def application(self,app={}):
        """ 
            return new application object or application object
            if typ(app) == int return app from api
                type(app) == dict return Application base on value in dict
                dict = {} return new app
        """
        return Application(self.key,self.secret,self.host,app)

    
    
    def api_users(self, app_id):
        """ 
            return collection of api_users object
            
        """
        return ApiUsers(self.key, self.secret, self.host, app_id)

    def api_user(self,app_id, api_user_id):
        """ return api user object"""
        return ApiUser(self.key,self.secret,self.host,app_id, api_user_id)

    def api_user_stats(self, app_id):
        """ 
            return collection of api_user_stat object
            
        """
        return ApiUserStats(self.key, self.secret, self.host, app_id)

    def api_user_stat(self,app_id, api_user_id):
        """ return api user object"""
        return ApiUserStat(self.key,self.secret,self.host,app_id, api_user_id)
 
    def entities(self,app_id):
        """
            return collection of entities object
        """
        return Entities(self.key,self.secret,self.host,app_id)

    def activities(self, app_id, activity_type):
        """
            return colection of any activity object by activity_type
        """
        return Activities(self.key, self.secret, self.host,app_id, activity_type)
 
    def view(self, app_id):
        """
            return colection of views object
        """
        return Activities(self.key, self.secret, self.host,app_id, 'view')
        

    def comment(self, app_id):
        """
            return colection of views object
        """
        return Activities(self.key, self.secret, self.host,app_id, 'comment')

    def like(self, app_id):
        """
            return colection of views object
        """
        return Activities(self.key, self.secret, self.host,app_id, 'like')
        

    def share(self, app_id):
        """
            return colection of views object
        """
        return Activities(self.key, self.secret, self.host,app_id, 'share')


 
