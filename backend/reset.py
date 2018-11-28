#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# reset controller

import json

class ResetController:
    def __init__(self, userdatabase, crypto_api):
        self.udb = userdatabase
        self.crypto = crypto_api
	
    def GET(self):
		self.udb.reset_data()
		return json.dumps({'result':'success'}) 
