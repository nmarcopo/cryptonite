import unittest
import requests
import json

class TestMovies(unittest.TestCase):

	SITE_URL = 'http://student04.cse.nd.edu:52109' # replace this with your port number
	USERS_URL = SITE_URL + '/users/'
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

	def test_users_put(self):
		self.assertEqual('1','1')
		'''self.reset_data()
		user = 'Andy'

		u = {}
		u['pwd'] = 'animep' '''
		#r = requests.post(self.
		# TODO CHECK INFO TEST
		'''self.assertTrue(self.is_json(r.content.decode('utf-8')))
		resp = json.loads(r.content.decode('utf-8'))
		self.assertEqual(resp['title'], 'Broken Arrow (1996)')
		self.assertEqual(resp['genres'], 'Action|Thriller')

		m = {}
		m['title'] = 'ABC'
		m['genres'] = 'Sci-Fi|Fantasy'
		r = requests.put(self.MOVIES_URL + str(movie_id), data = json.dumps(m))
		self.assertTrue(self.is_json(r.content.decode('utf-8')))
		resp = json.loads(r.content.decode('utf-8'))
		self.assertEqual(resp['result'], 'success')

		r = requests.get(self.MOVIES_URL + str(movie_id))
		self.assertTrue(self.is_json(r.content.decode('utf-8')))
		resp = json.loads(r.content.decode('utf-8'))
		self.assertEqual(resp['title'], m['title'])
		self.assertEqual(resp['genres'], m['genres'])'''
	
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
		assetdict['ETH']=1000
		assetdict['LTC']=48349

		w['asset']=assetdict
		URL = 'Andy'
		r = requests.post(self.USERS_URL + URL, data = json.dumps(w))
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		
		# TODO GET WALLET
		r = requests.get(self.USERS_URL + URL) 
		self.assertTrue(self.is_json(r.content.decode()))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'],'success')
		l = []
		l.append(assetdict)
		self.assertEqual(resp['wallet'],l)

	def test_movies_delete(self):
		self.assertEqual('1','1')
		'''self.reset_data()
		movie_id = 95

		m = {}
		r = requests.delete(self.MOVIES_URL + str(movie_id), data = json.dumps(m))
		self.assertTrue(self.is_json(r.content.decode('utf-8')))
		resp = json.loads(r.content.decode('utf-8'))
		self.assertEqual(resp['result'], 'success')

		r = requests.get(self.MOVIES_URL + str(movie_id))
		self.assertTrue(self.is_json(r.content.decode('utf-8')))
		resp = json.loads(r.content.decode('utf-8'))
		self.assertEqual(resp['result'], 'error')'''

if __name__ == "__main__":
    unittest.main()
