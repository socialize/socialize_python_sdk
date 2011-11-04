Socialize Python SDK
====================

How to use
----------

First time running you will need to activate the virtual environment to download
required package.


    ./build.sh build

    or modify the settings.py with verified partner key/secret.

    ./build.sh unit_test

    Or running tests using nosetests:

    _install/bin/nosetests [ -s for print output| -v more verbose ]

    
    

This SDK is a work in progress. Below are the implemented endpoints.


Partner API:

    partner/v1/application
        GET list of applications
        POST new application

    partner/v1/application/<id>
        GET specific application
        PUT update application information



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




