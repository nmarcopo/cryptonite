import asyncio
import requests
import json


# Austin Sura, just him

class _crypto_api:
    def __init__(self):
        self.apiBaseURL = "https://min-api.cryptocompare.com/data/"
        self.top15List = ["BTC","ETH","XRP","BCH","EOS","XLM","LTC","ADA","XMR","USDT","TRX","DASH","IOTA","TRX","DASH"]
        
    async def find_hottest_coldest(self, days, topN, mode):
        # get top 10 most increased value crypto
        # calculated by doing open on first day to close on last day
        coinDict = {}
        loop = asyncio.get_event_loop()
        awaitDict = {}
        for item in self.top15List:
            crypto_hottest_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(item, days)
            awaitDict[item] = loop.run_in_executor(None, requests.get, crypto_hottest_url)

        respDict = {}
        for key, val in awaitDict.items():
            respDict[key] = await val

        for key, val in respDict.items():
            resp = json.loads(val.content)
            cryptoDataDaysAgo = resp['Data'][0]['open']
            if cryptoDataDaysAgo == 0:
                continue
            cryptoDataToday = resp['Data'][days]['close']
            hotMeasurement = (cryptoDataToday - cryptoDataDaysAgo) / cryptoDataDaysAgo * 100
            coinDict[key] = hotMeasurement

        if mode == "hot":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=True)
        elif mode == "cold":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=False)
        else:
            print("please type 'hot' or 'cold'")
            return
        
        data = {}
        data['mode'] = mode
        for item, val in sorted_by_value[0:topN]:
            data[item] = "{:.2f}%".format(val)
            #print("{}: {:.2f}%".format(item, val))
        return json.dumps(data)

    async def what_if_investment(self, days, cryptosAndAmount):
        totalMoneyGained = 0
        crypto_code = []
        investment = []
        current = []
        loop = asyncio.get_event_loop()
        awaitDict = {}
        for crypto, amount in cryptosAndAmount.items():
            crypto_choice_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(crypto, days)
            r = requests.get(crypto_choice_url)
            resp = json.loads(r.content)
           # print(resp)
            cryptoDataDaysAgo = resp['Data'][0]['open']
            if cryptoDataDaysAgo == 0:
                print("This crypto, {}, didn't exist {} days ago. Not computing with this crypto.".format(crypto, days))
                continue 
            cryptoDataToday = resp['Data'][days]['close']
            crypto_code.append(crypto)
            investment.append(cryptoDataDaysAgo * amount)
            current.append(cryptoDataToday * amount)
       
        totalMoneyGained = sum(current) - sum(investment)
        percentChange = totalMoneyGained / sum(investment) * 100
        data={}
        data["Net Profit"]="{:.2f}".format(totalMoneyGained)
        data["Net Percentage"]="{:.2f}".format(percentChange)
        data["breakdown"]=[]
        #print("Net change: ${:.2f}, {:.2f}%".format(totalMoneyGained, percentChange))
        #print()
        for i in range(len(crypto_code)):
            mydict={}
            mydict["crypto"]=crypto_code[i]
            mydict["profit"]="{:.2f}".format(current[i]-investment[i])
            mydict["profit percentage"]="{:.2f}".format((current[i]-investment[i])/investment[i]*100)
            data["breakdown"].append(mydict)
            
        return json.dumps(data)
                



if __name__ == "__main__":
    test = _crypto_api()
    #test.what_if_investment(100, {'BTC':2, 'DBC':100})
    
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(test.find_hottest_coldest(10, 5, 'hot'))
    print(x)
