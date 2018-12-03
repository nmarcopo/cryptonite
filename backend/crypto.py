#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# crypto db controller

import json, cherrypy, asyncio, requests

class CryptoController:
    def __init__(self, _crypto_api):
        self.crypto = _crypto_api
    
    # Get top hottest or coldest crypto
    def POST_TOPN(self):
        output = {}
        try:
            payload = cherrypy.request.body.read()
            data = json.loads(payload)
            print(data)
            temp = data['temp']
            days = int(data['days'])
            count = data['count']
            static = data['static']
            if static == 'false':
                static = False
            elif static == 'true':
                static = True    
            preloaded = None
            if static:
                with open('hotcold.dat') as f:
                    data = f.readline().strip()
                    preloaded = json.loads(data)
            if static:
                response = self.crypto.find_hottest_coldest_static(days, count, temp, preloaded)
            else:
                response = self.crypto.find_hottest_coldest(days, count, temp)
            crypto_data = json.loads(response)
            output['result'] = 'success'
            output['crypto'] = crypto_data
            output['mode'] = temp
        except:
            output['result'] = 'error'
        return json.dumps(output)

    # Get crypto data
    def PUT(self):
        output = {}
        BASE_URL = "https://min-api.cryptocompare.com/data/"
        payload = cherrypy.request.body.read()
        data = json.loads(payload)
        cryptos = data['crypto']
        print(data)
        crypto_string = ','.join(cryptos)
        PRICE_URL = BASE_URL + "pricemulti?fsyms={}&tsyms=USD".format(crypto_string)
        try:
            r = requests.get(PRICE_URL)
            resp = r.json()
            for crypto in resp:
                output[crypto] = resp[crypto]['USD']
            output['result'] = 'success'
        except:
            output['result'] = 'error'
        return json.dumps(output)
 
    # Do what if investment
    def PUT_WHATIF(self):
        output = {}
        try:
            payload = cherrypy.request.body.read()
            data = json.loads(payload)
            asset = data['asset']                  # data['asset'] is a list
            preloaded = None
            if data['static'] != 'false':
                with open('whatif.dat') as f:
                    data = f.readline().strip()
                    preloaded = json.loads(data)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.crypto.what_if_investment(asset, preloaded))

            output = json.loads(response)
            output['result'] = 'success'
        except Exception as e:
            output['result'] = 'error'
        return json.dumps(output)
    
    # Get top5 Hottest
    def GET_TEMP(self, temp):
        output = {}
        try:
            temp = temp
            days = 10
            count = 5
            static = False
            response = self.crypto.find_hottest_coldest(days, count, temp)
            data = json.loads(response)
            output['result'] = 'success'
            output['data'] = data
        except:
            output['result'] = 'error'
        return json.dumps(output)
