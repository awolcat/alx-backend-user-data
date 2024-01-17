#!/usr/bin/env python3
"""Basic authentication class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth Base Class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if some route requires authentication
        """
        if path is None or excluded_paths is None:
            return True
        elif path in excluded_paths or f'{path}/' in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Returns value of request Authorization header
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user
        """
        return None
