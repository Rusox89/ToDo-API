""" Model defining module """
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, VARCHAR, BOOLEAN
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.engine import create_engine
from config import CURRENT_CONFIG

MODEL = declarative_base()


class Entry(MODEL):
    """ Defines a ToDo Entry """
    __tablename__ = "entry"

    entryid = Column(INTEGER, primary_key=True)
    userid = Column(INTEGER, ForeignKey('user.userid', ondelete="CASCADE"), nullable=False)
    title = Column(VARCHAR(128), nullable=False)
    completed = Column(BOOLEAN, default=False, nullable=False)
    description = Column(TEXT())
    user = relationship("User", back_populates="entries")

    def as_dict(self):
        return {
            'entryid': self.entryid,
            'userid': self.userid,
            'title': self.title,
            'completed': self.completed,
            'description': self.description
        }


class User(MODEL):
    """ Defines a user entry and logged user """
    __tablename__ = "user"

    userid = Column(INTEGER, primary_key=True)
    email = Column(VARCHAR(128), index=True)
    password = Column(VARCHAR(128))
    entries = relationship("Entry", back_populates="user", lazy="joined", cascade="all, delete-orphan")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)

def get_engine(
    proto,
    username,
    password,
    host,
    dbname
):
    """ creates the db connection """
    return create_engine(
        "{}://{}:{}@{}/{}".format(
            proto,
            username,
            password,
            host,
            dbname
        ),
        encoding="UTF8"
    )


def initialize_database(
        protocol=CURRENT_CONFIG.DB_PROTOCOL,
        username=CURRENT_CONFIG.DB_USERNAME,
        password=CURRENT_CONFIG.DB_PASSWORD,
        hostname=CURRENT_CONFIG.DB_HOSTNAME,
        database=CURRENT_CONFIG.DB_DATABASE
    ):
    """ Initializes the database if not initialized already """
    engine = get_engine(
        protocol,
        username,
        password,
        hostname,
        database
    )
    MODEL.metadata.create_all(engine)
    return engine


def get_session():
    """ Get the SA session """
    engine = get_engine(
        CURRENT_CONFIG.DB_PROTOCOL,
        CURRENT_CONFIG.DB_USERNAME,
        CURRENT_CONFIG.DB_PASSWORD,
        CURRENT_CONFIG.DB_HOSTNAME,
        CURRENT_CONFIG.DB_DATABASE
    )
    SessionClass = sessionmaker(bind=engine, autoflush=True)
    session = SessionClass()
    return session
