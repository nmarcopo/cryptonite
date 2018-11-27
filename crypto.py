#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# crypto db controller

import json, cherrypy, asyncio

class CryptoController:
    def __init__(self, _crypto_api):
        self.crypto = _crypto_api
    
    # Get top hottest or coldest crypto
    def GET_WALLET(self):
        payload = cherrypy.reqeust.body.read()
        data = json.loads(payload)
        temp = data['temp']
        days = data['days']
        count = data['count']
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.crypto.find_hottest_coldest(days, count, temp))
        response['result'] = 'success'
        return json.dumps(response)
    
    # Do what if investment
    def DELETE(self, days):
        output = {}
        payload = cherrypy.request.body.read()
        data = json.loads(payload)
        asset = data['asset'][0]                # data['asset'] is a list
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.crypto.what_if_investment(days, asset))
        response['result'] = 'success'
        return json.dumps(response) 
