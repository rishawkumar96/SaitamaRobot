import threading
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from SaitamaRobot.modules.sql import BASE, SESSION
from sqlalchemy import Boolean, Column, Integer, UnicodeText, DateTime

DATABASE_URL = "sqlite:///saitamarobot.db"

engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()

class AFK(BASE):
    __tablename__ = "afk_users"

    user_id = Column(Integer, primary_key=True)
    is_afk = Column(Boolean)
    reason = Column(UnicodeText)
    time = Column(DateTime)

    def __init__(self, user_id: int, reason: str = "", is_afk: bool = True):
        self.user_id = user_id
        self.reason = reason
        self.is_afk = is_afk
        self.time = datetime.now()

    def __repr__(self):
        return "afk_status for {}".format(self.user_id)


AFK.__table__.create(bind=engine, checkfirst=True)
INSERTION_LOCK = threading.RLock()

AFK_USERS = {}


def is_afk(user_id):
    return user_id in AFK_USERS


def check_afk_status(user_id):
    try:
        return SESSION.query(AFK).get(user_id)
    finally:
        SESSION.close()


def set_afk(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = AFK(user_id, reason, True)
        else:
            curr.is_afk = True

        AFK_USERS[user_id] = {"reason": reason, "time": curr.time}

        SESSION.add(curr)
        SESSION.commit()


def rm_afk(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if curr:
            if user_id in AFK_USERS:  # sanity check
                del AFK_USERS[user_id]

            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def toggle_afk(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = AFK(user_id, reason, True)
        elif curr.is_afk:
            curr.is_afk = False
        elif not curr.is_afk:
            curr.is_afk = True
        SESSION.add(curr)
        SESSION.commit()


def __load_afk_users():
    global AFK_USERS
    try:
        all_afk = SESSION.query(AFK).all()
        AFK_USERS = {
            user.user_id: {"reason": user.reason, "time": user.time} for user in all_afk if user.is_afk
        }
    finally:
        SESSION.close()


__load_afk_users()
