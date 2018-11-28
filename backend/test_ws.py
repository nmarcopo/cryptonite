#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Austin Sura, Andy Shin

import unittest
import requests
import json

class TestServer(unittest.TestCase):

	SITE_URL = 'http://student04.cse.nd.edu:52109' # replace this with your port number
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

	# ||||| User tests |||||||
	# VVVVV            VVVVVVV

	# checks GET request of non-existant user, which should return false
	def test_users_wallet_get(self):
		self.reset_data()
		r = requests.get(self.USERS_URL + 'DNE') 
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'error')
	
	# checks changing user id through a PUT request to USERS_URL+/change/
	def test_users_change(self):
		self.reset_data()
		# create a new user in database
		u={}
		u['user'] = 'chanheeSucks'
		u['pwd'] = 'peanuts'
		r = requests.post(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
	
		# create a new UID	
		u={}
		u['uid']= 'chanheeSucks'
		u['pwd'] = 'peanuts'
		u['newID']='andyRocks'
		r = requests.put(self.USERS_URL+'change/', data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		self.assertEqual(resp['new_id'],'andyRocks')

	# checks changing passwords through a PUT request to USERS_URL
	def test_users_pw_check(self):
		self.reset_data()
		# tests non-existant user
		u={}
		u['user'] = 'DNE'
		u['pwd'] = 'dne'
		r = requests.put(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'error')
			
	# tests POST request to create a new user in the database
	def test_users_post(self):
		self.reset_data()
		# creates a new user in database
		u = {}
		u['user'] = 'Andy'
		u['pwd'] = 'animep'
		r = requests.post(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		
		# checks if the user exists using PUT request
		r = requests.put(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		
	# tests PUT request to USERS_URL which checks first the existance of a username, and then that that password is correct	
	def test_users_password_put(self):
		self.reset_data()
		# creates a new user in database
		u = {}
		u['user'] = 'Andy'
		u['pwd'] = 'animep'
		r = requests.post(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')

		u = {}
		u['pwd'] = 'animep'
		u['new_pwd'] = 'mangap'
		r = requests.put(self.USERS_URL + 'Andy', data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')

		# Checks the new password using put which checks if the uid and password is valid
		u = {}
		u['user']= 'Andy'
		u['pwd']= 'mangap'
		r = requests.put(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')

	# checks POST request to add a cryptocurrency wallet to an existing user in database
	def test_users_wallet_post(self):
		self.reset_data()
		# creates a new user in database
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
		
		#adds wallet with POST request to NON-EXISTANT user (expects failure)
		w['asset']=assetdict
		URL = 'DNE'
		r = requests.post(self.USERS_URL + URL, data = json.dumps(w))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'error')

		# adds wallet with POST request to EXISTANT user (expects success)
		w['asset']=assetdict
		URL = 'Andy'
		r = requests.post(self.USERS_URL + URL, data = json.dumps(w))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		 
		
		# checks values of wallet with expected response
		r = requests.get(self.USERS_URL + URL) 
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		l = []
		l.append(assetdict)
		self.assertEqual(resp['wallet'],l)

	# checks PUT request to USERS_URL + change/ + UID to delete the user if the password is correct
	def test_user_delete(self):
		self.reset_data()
		# creates a new user in database
		u={}
		u['user'] = 'Andy'
		u['pwd'] = 'peanuts'
		r = requests.post(self.USERS_URL, data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		
		# tries to delete with wrong password, expects error
		u={}
		u['pwd'] = 'peanuts1'
		r = requests.put(self.USERS_URL+'change/'+'Andy', data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'error')
		
		# tries to delete with right password, expects success
		u={}
		u['pwd'] = 'peanuts'
		r = requests.put(self.USERS_URL+'change/'+'Andy', data = json.dumps(u))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')


	# ||||| Cryptos tests |||||||
	# VVVVV               VVVVVVV

	# checks PUT request of CRYPTO_URL to find a list of hottests cryptocurrencies in the past X-days
	def test_crypto_hottest_put(self):
		self.reset_data()
		
		d = {}
		d['temp'] = 'hot'
		d['days'] = 10
		d['count'] = 5
		d['static'] = True
		r = requests.put(self.CRYPTO_URL, data = json.dumps(d))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		# checks return value with preloaded expected values
		self.assertEqual(resp,{'result':'success','mode':'hot','BCH':'40.97%','XRP':'16.44%','XLM':'11.80%','DASH':'8.67%','ETH':'7.71%'})

	# checks PUT request of CRYPTO_URL + DAYS to find summary of a dict of cryptocurrencies that were invested DAYs days ago
	def test_crypto_if_put(self):
		self.reset_data()
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
		# checks return value with preloaded expected values
		self.assertEqual(resp,{'result':'success',"Net Profit": "-3327.38", "Net Percentage": "-20.24", "breakdown": [{"crypto": "BTC", "profit": "-3325.26", "profit percentage": "-20.23"}, {"crypto": "DBC", "profit": "-2.12", "profit percentage": "-73.81"}]})

if __name__ == "__main__":
    unittest.main()
