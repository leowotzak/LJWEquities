#!/usr/bin/env python
from dotenv import load_dotenv

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite+pysqlite:///:memory:', echo=True, future=True)
if __name__ == '__main__':

    load_dotenv()

