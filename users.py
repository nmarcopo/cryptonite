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
        uid = int(uid)
        if uid in self.udb.user_wallet:
            output = {'result':'success', 'id': uid}
            coin_list = []
            for coin, amount in self.udb.user_wallet[uid].items():
                coin = {}
                coin['name'] = coin
                coin['amount'] = amount
                coin_list.append(coin)
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
    def PUT(self, uid):
        output = {}
        payload = cherrypy.request.body.read()
        user_info = json.loads(payload)
        pwd = user_info['pwd']
        if self.udb.check_pwd(uid, pwd):
            output = {'result':'success'}
        else:
            output = {'result':'error'}
        return json.dumps(output) 
