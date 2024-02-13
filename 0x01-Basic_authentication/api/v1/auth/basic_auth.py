#!/usr/bin/env python3
"""Module containing auth class"""


from flask import request
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """Class for basic authenticaton"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str)\
            -> str:
        """gets bas64 authorization from header"""
        if not authorization_header\
                or not isinstance(authorization_header, str)\
            or not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """decodes base64 encoded str"""
        if not base64_authorization_header or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = b64decode(base64_authorization_header.encode("utf-8"))
            return decoded.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """extracts user credentials"""
        cred = decoded_base64_authorization_header
        if not cred or not isinstance(cred, str) or not ":" in cred:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """gets user"""
        if not user_email or not user_pwd or not isinstance(user_pwd, str)\
                or not isinstance(user_email, str):
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """gets current user"""
        authorisation = self.authorization_header(request)
        basic = self.extract_base64_authorization_header(authorisation)
        decoded = self.decode_base64_authorization_header(basic)
        cred = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(*cred)
        return user
