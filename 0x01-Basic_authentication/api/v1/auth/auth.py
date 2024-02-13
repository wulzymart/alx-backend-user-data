#!/usr/bin/env python3
"""
Module for authentication
"""


from typing import List, TypeVar
from flask import request


class Auth:
    """base class for different authenticaton
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns True if the path is not in the
        list of strings excluded_paths
        """
        if not path or not excluded_paths or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for p in excluded_paths:
            if p.startswith(path) or path.startswith(p):
                return False
            if p.endswith("*") and path.startswith(p[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
                request (_type_, optional): _description_. Defaults to None.

        Returns:
                str: _description_
        """
        if request is None:
            return None
        # get header from the request
        header = request.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """

        return None
