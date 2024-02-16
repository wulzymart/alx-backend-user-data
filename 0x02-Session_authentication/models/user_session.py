#!/usr/bin/env python3
""" User sessions Mpdule
"""


from models.base import Base


class UserSession(Base):
    """User Session model"""

    def __init__(self, *args: list, **kwargs: dict):
        """init class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id= kwargs.get('session_id')
