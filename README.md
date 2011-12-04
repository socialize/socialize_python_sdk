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
    
    Or running specific test

    _install/bin/nosetests -s -v tests.api_user_test:ApiUserTest.test_ban_user_by_id
    
    

This SDK is a work in progress. Below are the implemented endpoints.
 

Partner API:

    partner/v1/application
        - GET list of applications
        - POST new application

    partner/v1/application/<id>
        - GET specific application
        - PUT update application information
        - Delete
        - Upload P12 for push notification
        - Upload application icon

    partner/v1/api_user/
        - Get list of api_users [ filter by application ]
        - Get list of banned users

    partner/v1/api_user/<id>
        - ban
        - unban


Usage
-----

The client can be installed as a module and imported.

** You might need to add __init__.py in submodule root repo.

    Instruction from here http://chrisjean.com/2009/04/20/git-submodules-adding-using-removing-and-updating/

    to init:
    git submodule add git@github.com:socialize/socialize-python-sdk.git socialize_python_sdk
    git submodule init
    git submodule update
    
    #** I didn't add __init__.py into root folder because it will break every test
    #** I will try to fix it later
    
    touch socialize_python_sdk/__init__.py

    

    to update:
    goto submodule directory, 
    git submodule init
    git submodule update
    git pull



Examples:

    
    from socialize.client import Partner
    
    '''
        Partner interface can return
            - a list of applications
            - Single Application Object
    '''

    partner = Partner(key,secret,url)  
    apps = partner.applications(userId)

    for app in apps:
        print app
        print app.to_dict()

    # apps.find() return meta dict, list of application by userId
    meta, result = apps.find()
    
    # apps.findOne(id) return application object
    
    application = apps.findOne(42)




