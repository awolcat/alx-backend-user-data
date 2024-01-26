#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    USER_ATTRIBUTES = ['id', 'email', 'hashed_password',
                       'session_id', 'reset_token']

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add and persist a new user
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def check_attrs(self, **kwargs) -> bool:
        """Check allowed user attributes
        """
        for attr in kwargs.keys():
            if attr not in self.USER_ATTRIBUTES:
                return False
        return True

    def find_user_by(self, **kwargs) -> User:
        """Find user by some arbitrary key word arg
        """
        if not self.check_attrs(**kwargs):
            raise InvalidRequestError
        result = self._session.query(User).filter_by(**kwargs).first()
        if not result:
            raise NoResultFound
        # propagates to InvalidRequestError if unhandled
        return result

    def update_user(self, id, **kwargs) -> None:
        """Update user attributes
        """
        if not self.check_attrs(**kwargs):
            raise ValueError
        user = self.find_user_by(id=id)
        if 'id' in kwargs.keys():
            del kwargs['id']
        user.__dict__.update(**kwargs)
        self._session.commit()
        return None
