# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), lazy_tables=True)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
# auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')



######################################### 
## use fb auth ## for facebook "graphbook" application 
#########################################
import sys,os
from fbappauth import CLIENT_ID,CLIENT_SECRET
from facebook import GraphAPI, GraphAPIError
from gluon.contrib.login_methods.oauth20_account import OAuthAccount

################ 

## For Facebook Login

###############

class FaceBookAccount(OAuthAccount):
    """ OAuth impl for Facebook"""
    AUTH_URL="https://graph.facebook.com/oauth/authorize"
    TOKEN_URL="https://graph.facebook.com/oauth/access_token"
    def __init__(self,g):
        OAuthAccount.__init__(self,g,CLIENT_ID,CLIENT_SECRET,self.AUTH_URL,self.TOKEN_URL,
            scope='public_profile,email')
        self.graph=None
    def get_user(self):
        ''' Returns the user using the Graph api'''
        if not self.accessToken():
            return None
        if not self.graph:
            self.graph=GraphAPI((self.accessToken()))
            user=None

        try:
            args = {'fields' : 'id,first_name,last_name,email' }

            user=self.graph.get_object("me",**args)
        except GraphAPIError, e:
            self.session.token=None
            self.graph =None
        if user:
            print user
            return dict(first_name=user['first_name'], last_name=user['last_name'],
                username=user['id'],email=user['email'],password='default')

db.define_table('user',
    Field('email', length=128, label=T('Email'),unique=True, notnull=True),
    Field('mobile', length=10, label=T('Mobile No.')),
    Field('username', length=25, label=T('User name'), unique=True),
    Field('password', 'password', readable=True, label=T('Password'),),
    Field('user_type'),
    Field('dob', 'date', label=T('DOB')),
    Field('gender', 'string', label=T('Gender')),
    Field('first_name',length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('registration_key', length=512, writable=False, readable=False, default=''),
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),
    Field('registration_id', length=512, writable=False, readable=False, default=''),
    Field('otp_token','integer',writable=False, readable=False,notnull=False),
    Field('otp_last_count','integer',default=0,writable=False, readable=False), 
    Field('propic',default=''),
    Field('created_on','datetime',default=request.now),
    migrate=True,
    format= "%(first_name)s"
)

#his table should contain all the other attrbutes of a user related to diffrent modules
db.define_table('user_atrs',
    Field('user','reference user'),
    Field('blocked_bids','integer'),
    Field('prim_add','text'),
    Field('sec_add','text'),
    Field('prim_lat','string'),
    Field('prim_longi','string'),
    Field('sec_lat','string'),
    Field('sec_longi','string'),
    Field('user_stars'),
    Field('profile_img','upload'),
    Field('about_me','text'),
    Field('referal_code','string'),
    format="%(user)s"
    )


# Validating user-anle fields

db.user.username.requires = [IS_NOT_EMPTY(error_message = "Enter a Username!"), IS_NOT_IN_DB(db, db.user.username, error_message = "Username already exists!") ]
# db.user.password.requires = [IS_NOT_EMPTY(error_message = "Enter a Password!"),CRYPT()]
db.user.mobile.requires = [IS_NOT_EMPTY(error_message = "Enter a Mobile No.!"),IS_MATCH(r'^([7-9]{1})([0-9]{9})$', error_message=T('Enter a Valid phone number')),IS_NOT_IN_DB(db, db.user.mobile, error_message = "Mobile No. already exists!")]
db.user.email.requires = [IS_LOWER(),IS_EMAIL(error_message = "Invalid Email!"), IS_NOT_IN_DB(db, db.user.email, error_message = "Email ID already exists!")]
db.user.gender.requires = IS_IN_SET(('Male', 'Female',''))

custom_auth_table=db['user']

auth.settings.table_user = custom_auth_table
auth.settings.table_user_name = 'user'    #Very important to mention
auth.settings.table_group_name = 'user_group'
auth.settings.table_membership_name = 'user_membership'
auth.settings.table_permission_name = 'user_permission'
auth.settings.table_event_name = 'user_event'
auth.settings.table_cas_name='user_cas'

auth.settings.create_user_groups = None

auth.define_tables();

#################################

## FaceBookAccount

################################

# Activate Below lines when adding facebook authentication

# auth.settings.actions_disabled=['register',
#    'change_password','request_reset_password','profile']
# auth.settings.login_form=FaceBookAccount(globals())


auth.messages.invalid_login = 'Invalid login'
auth.messages.registration_verifying="Please verify your email"
auth.messages.unable_to_send_email="Unable to send verification mail, Please try again later"
auth.messages.email_sent='Please verify your email using the link sent to your Email address'
auth.messages.invalid_user = 'Invalid user'
auth.messages.email_verified="Thanks, Email Verified, Kindly Login"



## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.multi_login=True

auth.settings.password_min_length = 6

auth.settings.long_expiration = 3600*24*30 # one month
auth.settings.remember_me_form = True
auth.messages.label_remember_me = "Remember me (for 30 days)"




#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
