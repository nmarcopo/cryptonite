#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# user db controller

import json, cherrypy

class UserController:
    def __init__(self, _user_database):
        self.udb = _user_database
    
    # Get user wallet info
    def GET_WALLET(self, uid):
        output = {}
        if uid in self.udb.user_wallet:
            output = {'result':'success', 'id': uid}
            coin_list = []
            if self.udb.user_wallet[uid]:
                for item in self.udb.user_wallet[uid]:
                    coin_list.append(item)
                output['wallet'] = coin_list
        else:
            output = {'result':'error'}
        return json.dumps(output)
    
    # Change user id
    def PUT_CHANGE(self):
        output = {}
        payload = cherrypy.request.body.read()
        change_id = json.loads(payload)
        user_ID = change_id['user']
        pwd = change_id['pwd']
        newID = change_id['new_user']
        if self.udb.change_id(user_ID, newID, pwd):
            output = {'result':'success', 'new_user':newID}
        else:
            output = {'result':'error'}
        return json.dumps(output)
    
    # Check pwd
    def PUT_PWD(self):
        output = {}
        payload = cherrypy.request.body.read()
        user_info = json.loads(payload)
        uid = user_info['user']
        pwd = user_info['pwd']
        if self.udb.check_pwd(uid, pwd):
            output = {'result':'success'}
        else:
            output = {'result':'error'}
        return json.dumps(output)
    
    # Make new id
    def POST_ID(self):
        output = {}
        payload = cherrypy.request.body.read()
        new_id = json.loads(payload)
        uid = new_id['user']
        pwd = new_id['pwd']
        if self.udb.set_user(uid, pwd):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
    
    # Change password
    def PUT(self, uid):
        output = {}
        payload = cherrypy.request.body.read()
        change_pwd = json.loads(payload)
        curr_pwd = change_pwd['pwd']
        new_pwd = change_pwd['new_pwd']
        #old = self.udb[uid]
        if self.udb.change_pwd(uid, curr_pwd, new_pwd):
            #print(uid, self.udb[uid], old)
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
    
    # Add new data
    def POST(self, uid):
        output = {}
        payload = cherrypy.request.body.read()
        new_info = json.loads(payload)
        asset_dict = new_info['asset']
        if self.udb.add_sub_asset(uid, asset_dict):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)

    # Delete user
    def PUT_DELETE(self, uid):
        output = {}
        payload = cherrypy.request.body.read()
        pwd_info = json.loads(payload)
        pwd = pwd_info['pwd']
        if self.udb.delete_user(uid, pwd):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
