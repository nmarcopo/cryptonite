# crypto_api
# Austin Sura, Nicholas Marcopoli, Chan Hee Song, Sung Hyun Shin

import asyncio
import requests
import json

class _crypto_api:
    def __init__(self):
        self.apiBaseURL = "https://min-api.cryptocompare.com/data/"
        self.top15List = ["BTC","ETH","XRP","BCH","EOS","XLM","LTC","ADA","XMR","USDT","TRX","DASH","IOTA","TRX","DASH"]
        
    async def find_hottest_coldest(self, days, topN, mode, dataset=None):
        # get top 10 most increased value crypto
        # calculated by doing open on first day to close on last day
        loop = asyncio.get_event_loop()
        respDict = {}
        if dataset is None:
            for item in self.top15List:
                crypto_hottest_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(item, days)
                respDict[item] = await loop.run_in_executor(None, requests.get, crypto_hottest_url)
        else:
            respDict = dataset

        # Extract json response
        coinDict = {}
        for key, val in respDict.items():
            if dataset is None:
                resp = json.loads(val.content)
            else:
                resp = val
            try:
                cryptoDataDaysAgo = resp['Data'][0]['open']
            except IndexError:
                continue
            if cryptoDataDaysAgo == 0:
                continue
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
        #print(dataset)
        #print("what is this")
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
                resp = json.loads(val.content)
            else:
                resp = val
            cryptoDataDaysAgo = resp['Data'][0]['open']
            if cryptoDataDaysAgo == 0:
                continue 
            cryptoDataToday = resp['Data'][days]['close']
            crypto_code.append(key)
            amount = cryptosAndAmount[key]
            investment.append(cryptoDataDaysAgo * amount)
            current.append(cryptoDataToday * amount)
        
        # Format json output
        totalMoneyGained = sum(current) - sum(investment)
        percentChange = totalMoneyGained / sum(investment) * 100
        data={}
        data["Net Profit"]="{:.2f}".format(totalMoneyGained)
        data["Net Percentage"]="{:.2f}".format(percentChange)
        data["breakdown"]=[]
        for i in range(len(crypto_code)):
            mydict={}
            mydict["crypto"]=crypto_code[i]
            mydict["profit"]="{:.2f}".format(current[i]-investment[i])
            mydict["profit percentage"]="{:.2f}".format((current[i]-investment[i])/investment[i]*100)
            data["breakdown"].append(mydict)
            
        return json.dumps(data)
                
# Scratch space for the api
if __name__ == "__main__":
    test = _crypto_api()
    #with open("whatif.dat") as f:
    #    data = json.loads(f.readline().strip())
    #loop = asyncio.get_event_loop()
    #print(loop.run_until_complete(test.what_if_investment(100, {'BTC':2, 'DBC':100}, data)))

    #loop = asyncio.get_event_loop()
    #y = loop.run_until_complete(test.what_if_investment(100, {'BTC':2, 'DBC':100}))
    #print(y)
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(test.find_hottest_coldest(10, 5, 'hot'))
    print(x)
