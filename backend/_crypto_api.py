# crypto_api
# Austin Sura, Nicholas Marcopoli, Chan Hee Song, Sung Hyun Shin

import asyncio
import requests
import json

class _crypto_api:
    def __init__(self):
        self.apiBaseURL = "https://min-api.cryptocompare.com/data/"
        self.top15List = ["BTC","ETH","XRP","BCH","EOS","XLM","LTC","ADA","XMR","USDT","TRX","DASH","IOTA","BSV","XEM"]
    
    # find_hottest_coldest static version
    def find_hottest_coldest_static(self, days, topN, mode, dataset):
        # get top 10 most increased value crypto
        # calculated by doing open on first day to close on last day
        # use the static dataset
        respDict = dataset

        # Extract json response
        coinDict = {}
        for key, val in respDict.items():
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
        for item, val in sorted_by_value[0:topN]:
            data[item] = "{:.2f}%".format(val)
        return json.dumps(data)

    async def what_if_investment(self, cryptosAndAmount, dataset=None):
        totalMoneyGained = 0
        crypto_code = []
        investment = []
        current = []
        all_days = []
        awaitList = []
        awaitDict = {}
        return_days = []
        # If there is no pre-loaded dataset
        if not dataset:
            loop = asyncio.get_event_loop()
            # Call async request
            for crypto_dict in cryptosAndAmount:
                for crypto, args in crypto_dict.items():
                    days = int(args[0])
                    amount = int(args[1])
                    all_days.append([days, amount, crypto])
                    crypto_code.append(crypto)
                    crypto_choice_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(crypto, days)
                    awaitList.append(await loop.run_in_executor(None, requests.get, crypto_choice_url))
        else:
            awaitDict = dataset
            for crypto_dict in cryptosAndAmount:
                for crypto, args in crypto_dict.items():
                    all_days.append([int(args[0]), int(args[1]), crypto])
                    crypto_code.append(crypto)

        # Read json response if there is no preloaded dataset
        if not dataset:
            for key, val, args in zip(crypto_code, awaitList, all_days):
                # load in content if calling from the online api
                resp = json.loads(val.content)
                cryptoDataDaysAgo = resp['Data'][0]['open']
                if cryptoDataDaysAgo == 0:
                    continue
                cryptoDataToday = resp['Data'][args[0]]['close']
                # calculate amounts
                amount = args[1]
                investment.append(cryptoDataDaysAgo * amount)
                current.append(cryptoDataToday * amount)
                return_days.append(args[0])
        else:
            # if loading from static dataset
            j = 0
            for key, val in awaitDict.items():
                args = all_days[j]
                # don't load in content if calling from static database
                resp = val
                cryptoDataDaysAgo = resp['Data'][0]['open']
                if cryptoDataDaysAgo == 0:
                    continue 
                cryptoDataToday = resp['Data'][args[0]]['close']
                # calculate amounts
                amount = args[1]
                days = args[0]
                return_days.append(days)
                investment.append(cryptoDataDaysAgo * amount)
                current.append(cryptoDataToday * amount)
                j += 1

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
            mydict["days"] = return_days[i]
            data["breakdown"].append(mydict)
        return json.dumps(data)

    # Constantly cache hot and cold info every 10 mins
    def fetch_data(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.find_hottest_coldest_fetch())
        with open('crypto.dat', "w+") as f:
            json.dump(response, f)
    
    # Find hottest coldest data from cach
    def find_hottest_coldest(self, days, topN, mode):
        preloaded = {}
        coinDict = {}
        price_dict = {}
        with open('crypto.dat') as f:
            data = f.readline().strip()
            preloaded = json.loads(data)
        
        for key, val in preloaded.items():
            resp = val
            i = 2000 - days
            while resp['Data'][i]['open'] == 0:
                i += 1
            cryptoDataDaysAgo = resp['Data'][i]['open']
            cryptoDataToday = resp['Data'][1999]['close']
            hotMeasurement = (cryptoDataToday - cryptoDataDaysAgo) / cryptoDataDaysAgo * 100
            coinDict[key] = hotMeasurement
            price_dict[key] = cryptoDataToday
        
        if mode == "hot":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=True)
        elif mode == "cold":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=False)
        else:
            print("please type 'hot' or 'cold'")
            raise Exception
            return None 
        
        # Format output json
        data = []
        for item, val in sorted_by_value[0:topN]:
            data.append([item, "{:.2f}%".format(val), price_dict[item]])
        return json.dumps(data)
    
    # Actual helper async function to fetch data
    async def find_hottest_coldest_fetch(self):
        # calculated by doing open on first day to close on last day
        loop = asyncio.get_event_loop()
        respDict = {}
        returnDict = {}
        # call the api from online if no static dataset provided
        for item in self.top15List:
            crypto_hottest_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(item, 2000)
            respDict[item] = await loop.run_in_executor(None, requests.get, crypto_hottest_url)
            
        for key, val in respDict.items():
            resp = json.loads(val.content)
            returnDict[key] = resp
        
        return returnDict
