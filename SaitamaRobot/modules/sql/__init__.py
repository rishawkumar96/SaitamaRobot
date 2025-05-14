from SaitamaRobot.config import Development as Config
from SaitamaRobot import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI  # This line defines DATABASE_URL

BASE = declarative_base()

def start() -> scoped_session:
    engine = create_engine(DATABASE_URL, echo=False)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))

class BlacklistUsers(BASE):
    __tablename__ = 'blacklist_users'
    # define your columns here
      id = Column(Integer, primary_key=True)
# Create the table safely
BlacklistUsers.__table__.create(bind=engine, checkfirst=True)

BASE = declarative_base()
SESSION = start()
