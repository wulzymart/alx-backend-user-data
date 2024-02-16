#!/usr/bin/env python3
"""Module for session exp auth"""


from .session_exp_auth import SessionExpAuth
from models.user import User
from models.user_session import UserSession
from uuid import uuid4
from os import getenv
from datetime import datetime, timedelta



class SessionDBAuth(SessionExpAuth):
    """Session with db storage"""

    def create_session(self, user_id=None) -> str:
        """create and save session in db.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        entry = {"session_id": session_id, "user_id": user_id}
        user_session_db = UserSession(**entry)
        user_session_db.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """get user id but time considered"""

        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        if not session_id or session_id not in sessions:
            return None

        session = sessions[session_id]
        if self.session_duration > 0:
            if 'created_at' not in session:
                return None
            now = datetime.now()
            span = timedelta(seconds=self.session_duration)
            exp = session['created_at'] + span
            if exp < now:
                return None
        return session.get('user_id')
    
    def destroy_session(self, request=None) -> bool:
        """clears sessions from db"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
