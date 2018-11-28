#!/usr/bin/env python3
# User database
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura

import hashlib

class _user_database:
    def __init__(self):
        self.user_pwd = {}
        self.user_wallet = {}
    
    # Set user and pwd
    def set_user(self, user, pwd):
        if user not in self.user_pwd:
            self.user_pwd[user] = hashlib.sha3_512(pwd.encode()).hexdigest()
            self.user_wallet[user] = []
            return True
        else:
            return False
    
    # Check if password matches of the given user
    def check_pwd(self, user, pwd):
        if self.user_pwd[user] == hashlib.sha3_512(pwd.encode()).hexdigest():
            return True
        else:
            return False
    
    # Change password of the user
    def change_pwd(self, user, curr_pwd, new_pwd):
        if self.user_pwd[user] == hashlib.sha3_512(curr_pwd.encode()).hexdigest():
            self.user_pwd[user] = hashlib.sha3_512(new_pwd.encode()).hexdigest()
            return True
        return False
    
    # Change id of the user
    def change_id(self, user, newID, pwd):
        if self.user_pwd[user] == hashlib.sha3_512(pwd.encode()).hexdigest():
            self.user_pwd[newID] = self.user_pwd.pop(user)
            self.user_wallet[newID] = self.user_wallet.pop(user)
            return True
        return False
    
    # Delete user if password matches
    def delete_user(self, user, pwd):
        if user in self.user_pwd:
            if self.user_pwd[user] == hashlib.sha3_512(pwd.encode()).hexdigest():
                del self.user_pwd[user]
        if user in self.user_wallet:
            del self.user_wallet[user]
            return True
        return False
    
    # Manipulate user wallet
    def add_sub_asset(self, user, asset_dict):
        for coin, amount in asset_dict.items():
            if self.user_wallet[user] != []:
                for item in self.user_wallet[user]:
                    self.user_wallet[user].remove(item)
                    if coin in item:
                        item[coin] += amount
                    self.user_wallet[user].append(item)
            else:
                self.user_wallet[user].append(asset_dict)
    
    # Clear database
    def reset_data(self):
        self.user_pwd.clear()
        self.user_wallet.clear()
