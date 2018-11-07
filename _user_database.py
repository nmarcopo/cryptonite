#!/usr/bin/env python3
# User database
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura

import hashlib

class _user_database:
    def __init__(self):
        self.user_pwd = {}
        self.user_wallet = {}

    def set_user(self, user, pwd):
        self.user_pwd[user] = hashlib.sha1(pwd.encode()).hexdigest()
        self.user_wallet[user] = []

    def check_pwd(self, user, pwd):
        if self.user_pwd[user] == hashlib.sha1(pwd.encode()).hexdigest():
            return True
        else:
            return False

    def change_pwd(self, user, curr_pwd, new_pwd):
        if self.user_pwd[user] == hashlib.sha1(curr_pwd.encode()).hexdigest():
            self.user_pwd[user] = hashlib.sha1(new_pwd.encode()).hexdigest()
    
    def change_id(self, user, newID, pwd):
        if self.user_pwd[user] == hashlib.sha1(pwd.encode()).hexdigest():
            self.user_pwd[newID] = self.user_pwd.pop(user)
            self.user_wallet[newID] = self.user_wallet.pop(user)

    def delete_user(self, user, pwd):
        if user in self.user_pwd:
            if self.user_pwd[user] == hashlib.sha1(pwd.encode()).hexdigest():
                del self.user_pwd[user]
        if user in self.user_wallet:
            del self.user_wallet[user]

    def add_sub_asset(self, user, asset_dict):
        for coin, amount in asset_dict.items():
            for item in self.user_wallet[user]:
                if coin in item:
                    item[coin] += amount 

    def reset_data(self):
        self.user_pwd.clear()
        self.user_wallet.clear()
