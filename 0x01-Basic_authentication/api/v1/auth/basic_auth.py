#!/usr/bin/env python3
"""Basic Auth Class"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic authentication class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the value of the authorization header
            [a base64 encoded string]
        """
        if (authorization_header is None
                or type(authorization_header) is not str
                or authorization_header.startswith('Basic ') is False):
            return None
        auth_token = authorization_header.split(' ')[1]
        return auth_token

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of a Base64 string -
            base64_authorization_header
        """
        if (base64_authorization_header is None
                or type(base64_authorization_header) is not str):
            return None
        try:
            header = base64.b64decode(base64_authorization_header)
            return header.decode()  # decode bytes obj to str
        except Exception:
            return None
