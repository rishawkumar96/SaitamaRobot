import threading
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from SaitamaRobot.modules.sql import BASE, SESSION
from sqlalchemy import Column, String, UnicodeText

DATABASE_URL = "sqlite:///saitamarobot.db"


engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()

class BlacklistUsers(BASE):
    __tablename__ = "blacklistusers"
    user_id = Column(String(14), primary_key=True)
    reason = Column(UnicodeText)


def __init__(self, user_id, reason=None):
        self.user_id = user_id
        self.reason = reason

BASE.metadata.create_all(bind=engine)

BLACKLIST_LOCK = threading.RLock()
BLACKLIST_USERS = set()


def blacklist_user(user_id, reason=None):
    with BLACKLIST_LOCK:
        user = SESSION.query(BlacklistUsers).get(str(user_id))
        if not user:
            user = BlacklistUsers(str(user_id), reason)
        else:
            user.reason = reason

        SESSION.add(user)
        SESSION.commit()
        __load_blacklist_userid_list()


def unblacklist_user(user_id):
    with BLACKLIST_LOCK:
        user = SESSION.query(BlacklistUsers).get(str(user_id))
        if user:
            SESSION.delete(user)

        SESSION.commit()
        __load_blacklist_userid_list()


def get_reason(user_id):
    user = SESSION.query(BlacklistUsers).get(str(user_id))
    rep = ""
    if user:
        rep = user.reason

    SESSION.close()
    return rep


def is_user_blacklisted(user_id):
    return user_id in BLACKLIST_USERS


def __load_blacklist_userid_list():
    global BLACKLIST_USERS
    try:
        BLACKLIST_USERS = {int(x.user_id) for x in SESSION.query(BlacklistUsers).all()}
    finally:
        SESSION.close()


__load_blacklist_userid_list()
