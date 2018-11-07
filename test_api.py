#!/usr/bin/env python3
# Luke Song, Nick Marcopoli, Austin Sura, Andy Shin

from _crypto_api import _crypto_api
from _user_database import _user_database

import unittest
import hashlib

class TestAPIDatabase(unittest.TestCase):
        """unit tests for crypto API and user database"""

        #@classmethod
        #def setUpClass(self):
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
            self.assertEquals(user_pwd[0], 'Andy')
            self.assertEquals(user_pwd[1], hashlib.sha1('animep'.encode()).hexdigest())

        def test_check_pwd(self):
            self.udb.reset_data()
            self.udb.set_user('Nick', 'BTC')
            output = self.udb.check_pwd('Nick', 'BTC')
            self.assertEquals(output, True)

        def test_change_pwd(self):
            self.udb.reset_data()
            self.udb.set_user('Austin', 'XRP')
            self.udb.change_pwd('Austin', 'XRP', 'DASH')
            new_pwd = self.udb.user_pwd['Austin']
            self.assertEquals(new_pwd, hashlib.sha1('DASH'.encode()).hexdigest())

        def test_change_id(self):
            self.udb.reset_data()
            self.udb.set_user('Luke', 'USDP')
            self.udb.change_id('Luke', 'Andy', 'USDP')
            user_pwd = []
            for uid, pwd in self.udb.user_pwd.items():
                user_pwd.append(uid)
                user_pwd.append(pwd)
            self.assertEquals(user_pwd[0], 'Andy')
            self.assertEquals(user_pwd[1], hashlib.sha1('USDP'.encode()).hexdigest())

        def test_delete_user(self):
            self.reset_data()
            self.udb.set_user('Shreya', 'ETH')
            self.udb.delete_user('Shreya', 'ETH')
            self.assertEquals(self.udb.user_pwd, {})
            self.assertEquals(self.udb.user_wallet, {})

        def test_add_sub_asset(self):
            self.udb.reset_data()
            self.udb.set_user('Austin', 'XRP')
            self.udb.add_sub_asset('Austin', {'BTC':30})
            asset_list = []
            for coin, amount in self.udb.user_wallet['Austin'].items():
                asset_list.append(coin)
                asset_list.append(amount)
            self.assertEquals(asset_list[0], 'BTC')
            self.assertEquals(asset_list[1], 30)

if __name__ == "__main__":
    unittest.main()

