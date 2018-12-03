#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# user db controller

import json, cherrypy

class UserController:
    def __init__(self, _user_database):
        self.udb = _user_database
    
    # Get user wallet info
    def GET_WALLET(self, user):
        output = {}
        if user in self.udb.user_wallet:
            output = {'result':'success', 'id': user}
            coin_list = []
            if self.udb.user_wallet[user]:
                for item in self.udb.user_wallet[user]:
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
        user = user_info['user']
        pwd = user_info['pwd']
        if self.udb.check_pwd(user, pwd):
            output = {'result':'success'}
        else:
            output = {'result':'error'}
        return json.dumps(output)
    
    # Make new id
    def POST_ID(self):
        output = {}
        payload = cherrypy.request.body.read()
        new_id = json.loads(payload)
        user = new_id['user']
        pwd = new_id['pwd']
        if self.udb.set_user(user, pwd):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
    
    # Change password
    def PUT(self, user):
        output = {}
        payload = cherrypy.request.body.read()
        change_pwd = json.loads(payload)
        curr_pwd = change_pwd['pwd']
        new_pwd = change_pwd['new_pwd']
        if self.udb.change_pwd(user, curr_pwd, new_pwd):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
    
    # Add new data
    def POST(self, user):
        output = {}
        payload = cherrypy.request.body.read()
        new_info = json.loads(payload)
        asset_dict = new_info['asset']
        if self.udb.add_sub_asset(user, asset_dict):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)

    # Delete user
    def PUT_DELETE(self, user):
        output = {}
        payload = cherrypy.request.body.read()
        pwd_info = json.loads(payload)
        pwd = pwd_info['pwd']
        if self.udb.delete_user(user, pwd):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)

    # delete an item from the user's wallet
    def POST_DELETE(self, user):
        output = {}
        payload = cherrypy.request.body.read()
        data = json.loads(payload)
        coin = data['coin']
        user = user
        if self.udb.delete_item(user,coin):
            output['result'] = 'success'
        else:
            output['result'] = 'error'
        return json.dumps(output)
