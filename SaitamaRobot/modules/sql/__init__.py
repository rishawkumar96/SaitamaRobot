from SaitamaRobot.config import Development as Config
from SaitamaRobot import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String

DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI  # This line defines DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

BASE = declarative_base()

def start() -> scoped_session:
    engine = create_engine(DATABASE_URL, echo=False)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

class BlacklistUsers(BASE):
    __tablename__ = 'blacklist_users'
    # define your columns here
    user_id = Column(Integer, primary_key=True)
    
BASE.metadata.create_all(bind=engine)

BASE = declarative_base()
SESSION = start()
