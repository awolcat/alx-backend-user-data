#!/usr/bin/env python3
"""Bycrypt module"""
import bcrypt


def hash_password(pwd: str) -> bytes:
    """Hash user passwords.
        They should never be stored
        in plain text
    """
    # Unicode-objects must be encoded before hashing
    utf8_pwd = pwd.encode('UTF-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(utf8_pwd, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check password validity
    """
    password = password.encode('UTF-8')
    return bcrypt.checkpw(password, hashed_password)
