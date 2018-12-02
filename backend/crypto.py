#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# crypto db controller

import json, cherrypy, asyncio

class CryptoController:
    def __init__(self, _crypto_api):
        self.crypto = _crypto_api
    
    # Get top hottest or coldest crypto
    def PUT_TOPN(self):
        try:
            payload = cherrypy.request.body.read()
            data = json.loads(payload)
            temp = data['temp']
            days = data['days']
            count = data['count']
            static = data['static']
            if static:
                with open('hotcold.dat') as f:
                    preloaded = f.readline().strip()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.crypto.find_hottest_coldest(days, count, temp, json.loads(preloaded)))

            output = json.loads(response)
            output['result'] = 'success'
        except:
            output['result'] = 'error'
        return json.dumps(output)
    
    # Do what if investment
    def PUT(self, days):
        try:
            output = {}
            payload = cherrypy.request.body.read()
            data = json.loads(payload)
            asset = data['asset'][0]                # data['asset'] is a list
            #whatif.dat is preloaded data
            with open('whatif.dat') as f:
                preloaded = f.readline().strip()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.crypto.what_if_investment(int(days), asset, json.loads(preloaded)))

            output = json.loads(response)
            output['result'] = 'success'
        except:
            output['result'] = 'error'
        return json.dumps(output) 
