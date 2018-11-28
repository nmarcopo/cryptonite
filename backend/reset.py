#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# reset controller

import json

class ResetController:
    def __init__(self, userdatabase):
        self.udb = userdatabase
	
    # TODO should be a put
	def GET(self):
        self.udb.reset_data()
        return json.dumps({'result':'success'}) 
