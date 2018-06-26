# -*- coding:tf-8 -*-
__author__ = 'Maybe'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()

class TB(Base):
    __tablename__ = 'tmall'

    id = Column(Integer, primary_key=True)

