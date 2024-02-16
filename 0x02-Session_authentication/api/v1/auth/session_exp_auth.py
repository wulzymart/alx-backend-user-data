#!/usr/bin/env python3
"""Module for session exp auth"""


from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session with expiration"""

    def __init__(self) -> None:
        """initialize"""
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """add new session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """get user+id but time considered"""
        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session = self.user_id_by_session_id[session_id]
        if self.session_duration > 0:
            if 'created_at' not in session:
                return None
            now = datetime.now()
            span = timedelta(seconds=self.session_duration)
            exp = session['created_at'] + span
            if exp < now:
                return None
        return session.get('user_id')
