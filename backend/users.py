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
                    for coin, amount in item.items():
                        coin_dict = {}
                        coin_dict['name'] = coin
                        coin_dict['amount'] = amount
                        coin_list.append(coin_dict)
                output['wallet'] = coin_list
        else:
            output = {'result':'error'}
        return json.dumps(output)
    
    # Change user id
    def DELETE(self):
        output = {}
        payload = cherrypy.request.body.read()
        change_id = json.loads(payload)
        user_ID = change_id['uid']
        newID = change_id['newID']
        pwd = change_id['pwd']
        if self.udb.change_id(user_ID, newID, pwd):
            output = {'result':'success', 'new_id':newID}
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
        if self.udb.change_pwd(uid, curr_pwd, new_pwd):
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
        self.udb.add_sub_asset(uid, asset_dict)
        output['result'] = 'success'
        return json.dumps(output)

    # Delete user
    def DELETE_ID(self, uid):
        output = {}
        payload = cherrypy.request.body.read()
        pwd_info = json.loads(payload)
        pwd = pwd_info['pwd']
        if self.udb.delete_user(uid, pwd):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
