# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 23:23:59 2021

@author: Afonso
"""

from user import User
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# identidade única para Flask-JWT
def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)