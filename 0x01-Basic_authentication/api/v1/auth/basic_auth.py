#!/usr/bin/env python3
"""Basic Auth Class"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
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
        # print(f'decode {base64_authorization_header}')
        try:
            header = base64_authorization_header.encode('utf-8')
            header = base64.b64decode(header)  # raises binascii.Error-padding
            return header.decode('utf-8')  # decode bytes obj to str
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract user credentials from decoded authorization header

            Remember, Basic Authentication sets the Authorization header
            to the base64 encoding of username:password
        """
        if (decoded_base64_authorization_header is None
                or type(decoded_base64_authorization_header) is not str
                or ':' not in decoded_base64_authorization_header):
            return (None, None)
        user, password = decoded_base64_authorization_header.split(':')
        return (user, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Get user object from credentials
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
            if users is None or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get current user from request
        """
        header = self.authorization_header(request)
        try:
            token = self.extract_base64_authorization_header(header)
            decoded = self.decode_base64_authorization_header(token)
            email, password = self.extract_user_credentials(decoded)
            return self.user_object_from_credentials(email, password)
        except Exception as e:
            return
