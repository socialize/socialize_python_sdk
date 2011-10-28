Socialize Python SDK
====================

How to use
----------

This SDK is a work in progress. Below are the implemented endpoints.

    * Partner API
        Please check the tests/partner.py 


Usage
-----

The client can be installed as a module and imported.


Examples:

    from socialize.client import Partner
    
    partner = Partner(key,secret,url)  
    apps = partner.applications(userId)
    # apps.find() return meta dict, list of application
    meta, result = apps.find()
    # apps.findOne(id) return application object
    application = apps.findOne(42)




