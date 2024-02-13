#!/usr/bin/env python3
"""Module containing auth class"""


from flask import request, Request
from typing import List, TypeVar


class Auth:
    """base class for different authenticaton"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in the
        list of strings excluded_paths"""
        if not path:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        for p in excluded_paths:
            if path == p or (not path.endswith("/") and (path + "/") == p):
                return False
            if p.endswith("*") and path.startswith(p[: -1]):
                return False
        return True

    def authorization_header(self, request: Request = None) -> str:
        """
        If request is None, returns None
        If request doesn’t contain the header key Authorization, returns None
        Otherwise, return the value of the header request Authorization
        """
        if not request:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request: Request = None) -> TypeVar('User'):
        """gets current user object"""
        return None
