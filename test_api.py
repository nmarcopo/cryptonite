#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Austin Sura, Andy Shin

from _crypto_api import _crypto_api
from _user_database import _user_database

import unittest
import hashlib

class TestAPIDatabase(unittest.TestCase):
        """unit tests for crypto API and user database"""

        udb = _user_database()
        crypto_data = _crypto_api()

        def reset_data(self):
            "reset data is required because we cannot promise an order of test case execution"
            self.udb.reset_data()

        def test_set_user(self):
            self.udb.reset_data()
            self.udb.set_user('Andy', 'animep')
            user_pwd = []
            for uid, pwd in self.udb.user_pwd.items():
                user_pwd.append(uid)
                user_pwd.append(pwd)
            self.assertEqual(user_pwd[0], 'Andy')
            self.assertEqual(user_pwd[1], hashlib.sha1('animep'.encode()).hexdigest())
            
            result1 = self.udb.set_user('Andy', 'different')
            result2 = self.udb.set_user('Luke', 'hello')
            self.assertEqual(result1, False)
            self.assertEqual(result2, True)

        def test_check_pwd(self):
            self.udb.reset_data()
            self.udb.set_user('Nick', 'BTC')
            output = self.udb.check_pwd('Nick', 'BTC')
            self.assertEqual(output, True)

        def test_change_pwd(self):
            self.udb.reset_data()
            self.udb.set_user('Austin', 'XRP')
            self.udb.change_pwd('Austin', 'XRP', 'DASH')
            new_pwd = self.udb.user_pwd['Austin']
            self.assertEqual(new_pwd, hashlib.sha1('DASH'.encode()).hexdigest())

        def test_change_id(self):
            self.udb.reset_data()
            self.udb.set_user('Luke', 'USDP')
            self.udb.change_id('Luke', 'Andy', 'USDP')
            user_pwd = []
            for uid, pwd in self.udb.user_pwd.items():
                user_pwd.append(uid)
                user_pwd.append(pwd)
            self.assertEqual(user_pwd[0], 'Andy')
            self.assertEqual(user_pwd[1], hashlib.sha1('USDP'.encode()).hexdigest())

        def test_delete_user(self):
            self.reset_data()
            self.udb.set_user('Shreya', 'ETH')
            self.udb.delete_user('Shreya', 'ETH')
            self.assertEqual(self.udb.user_pwd, {})
            self.assertEqual(self.udb.user_wallet, {})

        def test_add_sub_asset(self):
            self.udb.reset_data()
            self.udb.set_user('Austin', 'XRP')
            self.udb.add_sub_asset('Austin', {'BTC':30})
            asset_list = []
            for item in self.udb.user_wallet['Austin']:
                for key, value in item.items():
                    asset_list.append(key)
                    asset_list.append(value)
            self.assertEqual(asset_list[0], 'BTC')
            self.assertEqual(asset_list[1], 30)

if __name__ == "__main__":
    unittest.main()

