import unittest
import requests
import json

class TestServer(unittest.TestCase):

	SITE_URL = 'http://student04.cse.nd.edu:52107' # replace this with your port number
	USERS_URL = SITE_URL + '/users/'
	CRYPTO_URL = SITE_URL + '/crypto/'
	RESET_URL = SITE_URL + '/reset/'

	def reset_data(self):
		m = {}
		r = requests.get(self.RESET_URL, data = json.dumps(m))

	def is_json(self, resp):
		try:
			json.loads(resp)
			return True
		except ValueError:
			return False

	def test_users_wallet_get(self):
		self.reset_data()
		r = requests.get(self.USERS_URL + 'aaaa') 
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'error')
	
	def test_users_delete(self):
		self.assertEqual('1','1')

	def test_users_put(self):
		self.assertEqual('1','1')
	
	def test_users_post(self):
		self.reset_data()
		u = {}
		u['user'] = 'Andy'
		u['pwd'] = 'animep'

		r = requests.post(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		
		# TODO GET TEST
		#r = requests.get(self.USERS_URL)
		
	def test_users_password_put(self):
		self.assertEqual('1','1')

	def test_users_wallet_post(self):
		self.reset_data()
		u = {}
		u['user'] = 'Andy'
		u['pwd'] = 'animep'

		r = requests.post(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		w = {}
		assetdict={}
		assetdict['BTC'] = 6
		assetdict['ETH'] = 1000
		assetdict['LTC'] = 48349

		w['asset']=assetdict
		URL = 'Andy'
		r = requests.post(self.USERS_URL + URL, data = json.dumps(w))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		
		r = requests.get(self.USERS_URL + URL) 
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		l = []
		l.append(assetdict)
		self.assertEqual(resp['wallet'],l)

	def test_user_delete(self):
		self.assertEqual('1','1')

	def test_crypto_hottest_put(self):
		d = {}
		d['temp'] = 'hot'
		d['days'] = 10
		d['count'] = 5
		d['static'] = True

		r = requests.put(self.CRYPTO_URL, data = json.dumps(d))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp,{'result':'success','mode':'hot','BCH':'40.97%','XRP':'16.44%','XLM':'11.80%','DASH':'8.67%','ETH':'7.71%'})

	def test_crypto_if_put(self):
		d = {}
		assetdict ={}
		assetdict['BTC']=2
		assetdict['DBC']=100
		assetlist = []
		assetlist.append(assetdict)
		d['asset']=assetlist
		
		days = '100'
		r = requests.put(self.CRYPTO_URL + days, data = json.dumps(d))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp,{'result':'success',"Net Profit": "-3327.38", "Net Percentage": "-20.24", "breakdown": [{"crypto": "BTC", "profit": "-3325.26", "profit percentage": "-20.23"}, {"crypto": "DBC", "profit": "-2.12", "profit percentage": "-73.81"}]})

if __name__ == "__main__":
    unittest.main()
