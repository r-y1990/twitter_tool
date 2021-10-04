from sqlalchemy import Column, String, BigInteger, DateTime, \
    create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
engine = create_engine('sqlite:///twitter.db', echo=True)


class Follower_data(Base):
    __tablename__ = 'follower_data'

    api_id = Column(BigInteger, primary_key=True)
    ins_date = Column(
        DateTime, default=datetime.datetime.utcnow, primary_key=True)
    api_id_str = Column(String, nullable=True)
    twitter_id = Column(String, nullable=True)
    name = Column(String, nullable=True)
    following = Column(Boolean, nullable=True)


Base.metadata.create_all(bind=engine)
