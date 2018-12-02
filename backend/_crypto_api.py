# crypto_api
# Austin Sura, Nicholas Marcopoli, Chan Hee Song, Sung Hyun Shin

import asyncio
import requests
import json

class _crypto_api:
    def __init__(self):
        self.apiBaseURL = "https://min-api.cryptocompare.com/data/"
        self.top15List = ["BTC","ETH","XRP","BCH","EOS","XLM","LTC","ADA","XMR","USDT","TRX","DASH","IOTA","BSV","XEM"]
        
    async def find_hottest_coldest(self, days, topN, mode, dataset=None):
        # get top 10 most increased value crypto
        # calculated by doing open on first day to close on last day
        loop = asyncio.get_event_loop()
        respDict = {}
        if dataset == None:
            # call the api from online if no static dataset provided
            for item in self.top15List:
                crypto_hottest_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(item, days)
                respDict[item] = await loop.run_in_executor(None, requests.get, crypto_hottest_url)
        else:
            # use the static dataset, if one is provided
            respDict = dataset

        # Extract json response
        coinDict = {}
        for key, val in respDict.items():
            if dataset is None:
                # need to load content if it came from online source
                resp = json.loads(val.content)
            else:
                # don't load content if it's a static database
                resp = val
            try:
                cryptoDataDaysAgo = resp['Data'][0]['open']
            except IndexError:
                # if the api ran out of free queries, skip that part of the data
                continue
            if cryptoDataDaysAgo == 0:
                continue
            # calculate the hot measurements
            cryptoDataToday = resp['Data'][days]['close']
            hotMeasurement = (cryptoDataToday - cryptoDataDaysAgo) / cryptoDataDaysAgo * 100
            coinDict[key] = hotMeasurement
        
        # Change output depending on top(hot) or low(cold)
        if mode == "hot":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=True)
        elif mode == "cold":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=False)
        else:
            print("please type 'hot' or 'cold'")
            raise Exception
            return None
        
        # Format output json
        data = {}
        data['mode'] = mode
        for item, val in sorted_by_value[0:topN]:
            data[item] = "{:.2f}%".format(val)
        return json.dumps(data)

    async def what_if_investment(self, days, cryptosAndAmount, dataset=None):
        totalMoneyGained = 0
        crypto_code = []
        investment = []
        current = []
        awaitDict = {}
        # If there is no pre-loaded dataset
        if not dataset:
            loop = asyncio.get_event_loop()
            # Call async request
            for crypto, amount in cryptosAndAmount.items():
                crypto_choice_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(crypto, days)
                awaitDict[crypto] = await loop.run_in_executor(None, requests.get, crypto_choice_url)
        else:
            awaitDict = dataset

        # Read json response 
        for key, val in awaitDict.items():
            if not dataset:
                # load in content if calling from the online api
                resp = json.loads(val.content)
            else:
                # don't load in content if calling from static database
                resp = val
            cryptoDataDaysAgo = resp['Data'][0]['open']
            if cryptoDataDaysAgo == 0:
                continue 
            cryptoDataToday = resp['Data'][days]['close']
            crypto_code.append(key)
            # calculate amounts
            amount = cryptosAndAmount[key]
            investment.append(cryptoDataDaysAgo * amount)
            current.append(cryptoDataToday * amount)
        
        # Format json output
        # calculate money gained (or lost) and percentage changed
        totalMoneyGained = sum(current) - sum(investment)
        percentChange = totalMoneyGained / sum(investment) * 100
        data={}
        data["Net Profit"]="{:.2f}".format(totalMoneyGained)
        data["Net Percentage"]="{:.2f}".format(percentChange)
        data["breakdown"]=[]
        # build the json
        for i in range(len(crypto_code)):
            mydict={}
            mydict["crypto"]=crypto_code[i]
            mydict["profit"]="{:.2f}".format(current[i]-investment[i])
            mydict["profit percentage"]="{:.2f}".format((current[i]-investment[i])/investment[i]*100)
            data["breakdown"].append(mydict)
            
        return json.dumps(data)

    # Constantly fetch hot and cold info every 10 mins
    def fetch_data(self):
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.crypto.find_hottest_coldest(500, 15, 'hot', None))
        output = json.loads(response)
        with open('crypto.dat') as f:
            json.dump(output, f)
        pass
        
