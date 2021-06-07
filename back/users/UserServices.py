# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, redirect, request, session
import logging
from uuid import uuid4

from back.tools.Tools import ToolManager
from flask import send_file
import hashlib
import sqlite3

import io

from back.tools.Tools import DbManager

logger = logging.getLogger(__name__)

u"""
**************************************************
ui layer
"""

users_page = Blueprint('users_page', __name__,
                       template_folder='templates', static_folder='static')

@users_page.route('/apiv1.0/admin/initDB', methods=['GET'])
def getInitDB():
    tmgr = ToolManager()
    tmgr.createDb()
    return jsonify({'DBcreated': "yes"})


@users_page.route('/apiv1.0/users', methods=['GET'])
def getusers():
    u"""
    return the complete list of users sorted by nickName and eventually filtered by 'validated'
    :return: collection of users in jso format
    """
    filterValidated=request.args.get('validated')
    mgr = UserManager()
    users = mgr.getAllUsers(filterValidated)
    logger.info("getusers::users={}".format(users))
    return jsonify({'users': users})


@users_page.route('/apiv1.0/users/<user_id>', methods=['GET', 'POST'])
def getuser(user_id):
    u"""
    main route for user
    :param user_id: uuid
    :return: user in json format
    """
    logger.info("getuser::API USER:: user_id={} / method={}".format(user_id, request.method))
    mgr = UserManager()
    user = mgr.getUserByUserId(user_id)
    if request.method == 'POST':
        userFromClient = request.json["connect"]
        #call Service (DAO)
        logger.info(u'saveuser::userid={}'.format(user.user_id))
        logger.info(u'saveuser::userFromClient={}'.format(userFromClient))
        checkRight=False
        #first connection
        if user.nickName == "" and user.description == "":
            logger.info("nickName &nd descrption are None - First subscription")
            checkRight=True
        else:
            if "cookieUserKey" in session:
                cookieUserKey = session['cookieUserKey']
                logger.info(u"getuser::cookieUserKey={}".format(cookieUserKey))
                if (user.user_id==cookieUserKey):
                    checkRight=True
                else:
                    userFromCookie = mgr.getUserByUserId(cookieUserKey)
                    if (userFromCookie.isAdmin):
                        checkRight=True
        if (checkRight):
            if "thepwd" in userFromClient:
                logger.info("thepwd set")
                mgr.saveUser(user.email, userFromClient["nickName"],
                            userFromClient["description"], user.user_id, user.validated,
                            userFromClient["thepwd"])
            else:
                logger.info("thepwd NOT set")
                mgr.saveUser(user.email, userFromClient["nickName"],
                    userFromClient["description"], user.user_id, user.validated,
                    "")

            return jsonify({'user': request.json["connect"]})
        else:
            return "Ha ha ha ! Mais t'es pas la bonne personne pour faire ça, mon loulou", 403
    else:
        #= GET
        logger.info("getuser::uuid={} - user={}".format(user_id, user))
        return jsonify({'user': user.__dict__})


@users_page.route('/subscription', methods=['POST'])
def subscriptionPost():
    u"""
    first step of subscription : store user in db  and email send (before user validation)
    :return: forward to a page (not angular style : TODO change it if necessary)
    """
    logger.info("subscriptionPost")
    connect = request.json["connect"]
    logger.info(u"subscriptionPost::connect:{}".format(connect))
    email=connect["email"]
    logger.info(u"subscriptionPost::email:{}".format(email))
    mgr = UserManager()
    user = mgr.getUserByEmail(email)
    if user is None:
        tool = ToolManager()
        #ne email send because of SPAM wall
        uuid = str(uuid4())
        logger.info(u"subscriptionPost::new user:: need new user_id:{}".format(uuid))
        mgr.saveUser(email, "", "", uuid, False, "")
        logger.info(u"\tsubscriptionPost::save done : return uuid={}".format(uuid))
        return jsonify({'uuid': uuid})
    else:
        if user.validated:
            tool_mgr = ToolManager()
            url_root = tool_mgr.getProperty("url_root")["value"]
            return redirect("{}".format(url_root))
        else:
            tool_mgr = ToolManager()
            url_root = tool_mgr.getProperty("url_root")["value"]
            urlcallback = u"{}/users/{}/confirmation".format(url_root, user.user_id)
            return redirect("{}".format(urlcallback))

@users_page.route('/<user_id>/confirmation', methods=['GET'])
def confirmationSubscription(user_id):
    u"""
    url called from email to confirm subscription
    :return: redirect to user detail page (normal not return json data as angular style because user
    is in its email client and not in our site)
    """
    logger.info("confirmationSubscription")
    logger.info(u"confirmationSubscription::user_id:{} ".format(user_id))
    tool = ToolManager()
    #sg = tool.get_sendgrid()

    mgr = UserManager()
    user = mgr.getUserByUserId(user_id)
    logger.info(u'confirmationSubscription::user={}'.format(user))

    mgr.saveUser(user.email, user.nickName, user.description, user.user_id, True, "")

    
    tool_mgr = ToolManager()
    url_root = tool_mgr.getProperty("url_root")["value"]
    
    # from_email = Email("eurommxvi.foot@gmail.com")
    # to_email = Email(user.email)
    # subject = "phipha2018 - confirmation"
    # content = Content("text/html", "<html><head></head><body><h1><a href='{}'>Congratulations on your registration ! </a></h1></hr></body></html>")
    # mail = Mail(from_email, subject, to_email, content)
    # response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)


    return redirect("{}/#!/user_detail/{}/?firstConnection=true".format(url_root,user_id))

@users_page.route('/apiv1.0/login', methods=['POST'])
def login():
    logger.info("login::API LOGIN:: param={}/ method={}".format(request.json, request.method))
    connect = request.json["connect"]
    logger.info("login::connect={}".format(connect))
    mgr = UserManager()
    user = mgr.authenticate(connect["email"], connect["thepwd"])
    logger.info("login::auth user={}".format(user))
    if (user is None):
        return "not authenticated", 401
    else:
        logger.info("login::push cookies={}".format(user.user_id))
        session['cookieUserKey'] = user.user_id
        return jsonify({'user': user.__dict__}), 200


# For a given file, return whether it's an allowed type or not
def allowed_file_type(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['jpg','jpeg','JPG', 'JPEG'])

@users_page.route('/apiv1.0/users/<user_id>/avatar', methods=['POST'])
def saveAvatar(user_id):
    u"""
    Save the avatar
    :param user_id: uuid
    :return: the http status
    """
    checkRight=False
    if "cookieUserKey" in session:
        cookieUserKey = session['cookieUserKey']
        if (user_id==cookieUserKey):
            checkRight=True
        mgr = UserManager()
        userFromCookie = mgr.getUserByUserId(cookieUserKey)
        if (userFromCookie.isAdmin):
            checkRight=True
    if (checkRight):
        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file_type(file.filename):

            data = file.read()
            file.close()

            # check the length (500Ko max)
            if len(data) < 500000:
                mgr = UserManager()
                avatarId = mgr.saveAvatar(user_id, data)
                return "Yes !", 200
            else:
                return "Size of the file ("+str(len(data))+" ko) more than 500 Ko", 415
        else:
            return "Non supported file (jpg/jpeg mandatory)", 413
    else:
        return "Ha ha ha ! Mais t'es pas la bonne personne pour faire ça, mon loulou", 403


@users_page.route('/apiv1.0/users/<user_id>/avatar', methods=['GET'])
def getAvatar(user_id):
    u"""
    Get the avatar
    :param user_id: uuid
    :return: the avatar
    """
    mgr = UserManager()
    avatar = mgr.getAvatar(user_id)

    if avatar is None:
        return send_file('static/img/avatar/default_avatar.png',mimetype='image/png');
    else:
        return send_file(io.BytesIO(avatar),mimetype='image/jpg', cache_timeout=0, add_etags=True)

"""
users_page= remove cookieUserKey
"""
@users_page.route('/apiv1.0/logout', methods=['POST'])
def logout():
    logger.info(u"API LOGOUT::logout - remove ={}".format(session['cookieUserKey']))
    del session['cookieUserKey']
    return u"Good bye", 200


u"""
**************************************************
Service layer
"""

class User:

    def __init__(self):
        self.description = u""
        self.email = u""
        self.nickName = u""
        self.user_id=u""
        self.validated = False
        self.pwd=u""
        self.isAdmin=u""


    def convertFromDB(self, elt):
        """
        convert a User object from db
        """
        if 'description' in elt.keys():
            self.description = elt['description']
        if 'email' in elt.keys():
            self.email = elt['email']
        if 'nickName' in elt.keys():
            self.nickName = elt['nickName']
        if 'uuid' in elt.keys():
            self.user_id = elt['uuid']
        if 'validated' in elt.keys():
            self.validated = elt['validated']
        if 'hashedpwd' in elt.keys():
            self.pwd= elt['hashedpwd']
        if 'isAdmin' in elt.keys():
            self.isAdmin= elt['isAdmin']
        else:
            self.isAdmin=False

    def convertIntoDB(self):
        """
        convert a User object into mongo Bson format
        """
        elt = dict()
        #elt['_id'] = self._id
        elt['description'] = self.description
        elt['email'] = self.email
        elt['nickName'] = self.nickName
        elt['uuid'] = self.user_id
        elt['validated'] = self.validated
        elt['hashedpwd'] = self.pwd
        elt['isAmin'] = self.isAdmin
        return elt

class UserManager(DbManager):


    def getAllUsers(self,filterValidated):
        """ get the list of users"""
        localdb = self.getDb()
        logger.info(u'getAllUsers::db={}'.format(localdb))
        logger.info(u'getAllUsers::row_factory={}'.format(localdb.row_factory))

        """uuid, nickName, desc, avatar, email, isAdmin"""

        sql_all_tab="""SELECT uuid, nickName, description, avatar, email, isAdmin, validated
                        FROM BETUSER order by nickName;"""
        #localdb.row_factory = self.dict_factory
        logger.info(u'getAllUsers::row_factory={}'.format(localdb.row_factory))
        cur = localdb.cursor()
        cur.execute(sql_all_tab)

        rows = cur.fetchall()
        usersList=list()
        for row in rows:
            if (filterValidated ):
                if row["validated"]==1:
                    usersList.append(row)                    
            else:
                usersList.append(row)
            logger.info(row)
        
        return usersList

    def hash_password(self,password):
        # uuid is used to generate a random number
        salt = uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def saveUser(self, email, nickName, description, user_id, validated, pwd):
        """ save a user"""
        localdb = self.getDb()
        usr = self.getUserByUserId(user_id)
        logger.info(u'saveUser::{} trouve ? usr ={}'.format(user_id, usr ))
        try:            
            c = localdb.cursor()
            if (usr is None):
                usr=User()
                usr.email=email
                usr.description=description
                usr.nickName=nickName
                usr.validated=validated        
                usr.user_id=user_id                
                c.execute("""insert into BETUSER 
                    (uuid, nickName, email,description, validated )
                    values
                    ('{}', '{}','{}', '{}', '{}');""".format(user_id, nickName,email, description, validated))            
            else:
                logger.info(u'\t try update to user : {} '.format(usr.user_id))
                usr.email=email
                usr.description=description
                usr.nickName=nickName
                usr.validated=validated        
                if (pwd != ""):
                    c.execute("""update BETUSER 
                    set nickName='{}', email='{}',description='{}', validated='{}', hashedpwd='{}'
                    where
                    uuid='{}'""".format(nickName,email, description, validated, self.hash_password(pwd), user_id))            

                else:
                    c.execute("""update BETUSER 
                    set nickName='{}', email='{}',description='{}', validated='{}'
                    where
                    uuid='{}'""".format(nickName,email, description, validated, user_id))            
            
            localdb.commit()
            logger.info(u'saveUser::commit')
            
        except sqlite3.Error as e:
            logger.error(e)
            logger.info(u'\tid : {}'.format(user_id))
            localdb.rollback()
            logger.info(u'saveUser::rollback')
            usr=None
            
        return usr

    def getUserByEmail(self, email):
        """ get one user by email"""
        localdb = self.getDb()
        logger.info(u'getUserByEmail::email={}'.format(email))

        sql="""SELECT uuid, nickName, description, avatar, email, isAdmin, validated, hashedpwd
                        FROM BETUSER where email='{}' ;"""
        cur = localdb.cursor()        
        cur.execute(sql.format(email))

        row = cur.fetchone()
        logger.info(u'getUserByEmail::user={}'.format(row))
        if row is not None:
            user = User()
            user.convertFromDB(row)
            return user
        else:
            return None

    def getUserByUserId(self, user_id):
        """ get one user by userid"""
        localdb = self.getDb()
        logger.info(u'getUserByUserId::user_id={}'.format(user_id))

        sql="""SELECT uuid, nickName, description, avatar, email, isAdmin, validated, hashedpwd
                        FROM BETUSER where uuid='{}' ;"""
        cur = localdb.cursor()        
        cur.execute(sql.format(user_id))

        row = cur.fetchone()
        logger.info(u'getUserByUserId::user={}'.format(row))
        if row is not None:
            user = User()
            user.convertFromDB(row)
            return user
        else:
            logger.info(u'getUserByUserId::not found !')
            return None

    def check_password(self,hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    def authenticate(self, email, pwd):
        """ authenticate user and retrieve it if ok"""
        localdb = self.getDb()
        logger.info(u'authenticate::email={}/pwd={}'.format(email, pwd))

        user = self.getUserByEmail(email)
        #logger.info(u'authenticate::bsonUser={}'.format(bsonUser))
        #bsonUser=dict()
        if user is not None:
            logger.info(u'authenticate::hashed user.pwd={}'.format(user.pwd))
            if self.check_password(user.pwd, pwd):
                logger.info(u'authenticated::user={}'.format(user))
                return user
            else:
                return None
        else:
            return None
        
    def saveAvatar(self,user_id, file):
        """ save an avatar in DB"""

        localdb = self.getDb()

        avatarFromDB = localdb.avatars.find_one({"avatar_user_id": user_id})

        if avatarFromDB is None:
            bsonAvatar =dict()
            bsonAvatar["avatar_user_id"]=user_id
            bsonAvatar["file"] = Binary(file,0)
            #logger.info(u'\t**** CREATION : {}'.format(bsonAvatar))
            logger.info(u'\t**** CREATION ****')
            localdb.avatars.insert_one(bsonAvatar)
        else:
            #logger.info(u'\t**** UPDATE : {}'.format(avatarFromDB))
            logger.info(u'\t**** UPDATE ****')
            localdb.avatars.update({"_id":avatarFromDB["_id"]},
                                            {"$set":{"file":Binary(file,0)}}, upsert=True)
        return user_id

    def getAvatar(self,user_id):
        """ get an avatar in DB"""

        localdb = self.getDb()

        avatarFromDB = localdb.avatars.find_one({"avatar_user_id": user_id})

        if avatarFromDB is None:
            return None
        else:
            return avatarFromDB["file"]

    def getUsersByUserIdList(self, user_id_tab):
        """ get a userlist by useridlist """
        localdb = self.getDb()
        logger.info(u'getUserByUserIdList::user_id_list={}'.format(user_id_tab))

        usersList = localdb.users.find({"user_id": {"$in": user_id_tab}})

        result = list()

        for userbson in usersList:
            user = User()
            user.convertFromDB(userbson)
            logger.info(u'\tgetUsersByUserIdList::user={}'.format(user))
            tmpdict = user.__dict__
            logger.info(u'\tgetUsersByUserIdList::tmpdict={}'.format(tmpdict))
            result.append(tmpdict)
        return result