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
            preloaded = None
            if static:
                with open('hotcold.dat') as f:
                    data = f.readline().strip()
                    preloaded = json.loads(data)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.crypto.find_hottest_coldest(days, count, temp, preloaded))

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
            preloaded = None
            with open('whatif.dat') as f:
                data = f.readline().strip()
                preloaded = json.loads(data)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.crypto.what_if_investment(int(days), asset, preloaded))

            output = json.loads(response)
            output['result'] = 'success'
        except:
            output['result'] = 'error'
        return json.dumps(output) 
