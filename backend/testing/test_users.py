import unittest
import requests
import json

class TestMovies(unittest.TestCase):

    SITE_URL = 'http://student04.cse.nd.edu:52111' # replace this with your port number
    MOVIES_URL = SITE_URL + '/movies/'
    RESET_URL = SITE_URL + '/reset/'

    def reset_data(self):
    m = {}
r = requests.put(self.RESET_URL, data = json.dumps(m))

def is_json(self, resp):
try:
    json.loads(resp)
    return True
except ValueError:
    return False

    def test_movies_get(self):
    self.reset_data()
movie_id = 32
r = requests.get(self.MOVIES_URL + str(movie_id))
self.assertTrue(self.is_json(r.content.decode('utf-8')))
resp = json.loads(r.content.decode('utf-8'))
self.assertEqual(resp['title'], 'Twelve Monkeys (1995)')
self.assertEqual(resp['genres'], 'Drama|Sci-Fi')
self.assertEqual(resp['img'], '/vxiIABQhiFlfODwamoevrzXvowU.jpg')

def test_movies_put(self):
self.reset_data()
movie_id = 95

r = requests.get(self.MOVIES_URL + str(movie_id))
self.assertTrue(self.is_json(r.content.decode('utf-8')))
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
self.assertEqual(resp['genres'], m['genres'])

def test_movies_delete(self):
self.reset_data()
movie_id = 95

m = {}
r = requests.delete(self.MOVIES_URL + str(movie_id), data = json.dumps(m))
self.assertTrue(self.is_json(r.content.decode('utf-8')))
resp = json.loads(r.content.decode('utf-8'))
self.assertEqual(resp['result'], 'success')

r = requests.get(self.MOVIES_URL + str(movie_id))
self.assertTrue(self.is_json(r.content.decode('utf-8')))
resp = json.loads(r.content.decode('utf-8'))
self.assertEqual(resp['result'], 'error')

if __name__ == "__main__":
    unittest.main()
