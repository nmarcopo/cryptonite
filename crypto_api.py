import requests
import json


# Austin Sura, just him

class _crypto_api:
    def __init__(self):
        self.apiBaseURL = "https://min-api.cryptocompare.com/data/"
        self.top15List = ["BTC","ETH","XRP","BCH","EOS","XLM","LTC","ADA","XMR","USDT","TRX","DASH","IOTA","TRX","DASH"]
        
    def find_hottest_coldest(self, days, topN, mode):
        # get top 10 most increased value crypto
        # calculated by doing open on first day to close on last day
        coinDict = {}
        for item in self.top15List:
            crypto_hottest_url = self.apiBaseURL + "histoday?fsym={}&tsym=USD&limit={}".format(item, days)
            r = requests.get(crypto_hottest_url)
            resp = json.loads(r.content)
            cryptoDataDaysAgo = resp['Data'][0]['open']
            if cryptoDataDaysAgo == 0:
                #print(item)
                continue
            cryptoDataToday = resp['Data'][days]['close']
            hotMeasurement = (cryptoDataToday - cryptoDataDaysAgo) / cryptoDataDaysAgo * 100
            coinDict[item] = hotMeasurement
        if mode == "hot":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=True)
        elif mode == "cold":
            sorted_by_value = sorted(coinDict.items(), key=lambda kv: kv[1], reverse=False)
        else:
            print("please type 'hot' or 'cold'")
            return
        #print(sorted_by_value)
        data={}
        data["mode"]=mode
        for item, val in sorted_by_value[0:topN]:
            #print("{}: {:.2f}%".format(item, val))
            data[item]=val
        return json.dumps(data)


    def what_if_investment(self, days, cryptosAndAmount):
        totalMoneyGained = 0
        crypto_code = []
        investment = []
        current = []
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
    mydata= test.what_if_investment(100, {'BTC':2, 'DBC':100})
    myjson=test.find_hottest_coldest(10,3,"hot")
    print(mydata)
    print(myjson)
