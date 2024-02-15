#!/usr/bin/env python3
"""Module containing session auth class"""


from flask import request
from typing import TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class SessionAuth(Auth):
    """implement Session Auth"""
    pass
