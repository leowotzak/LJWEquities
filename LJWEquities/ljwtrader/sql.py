#!/usr/bin/env python
from dotenv import load_dotenv

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
if __name__ == '__main__':

    load_dotenv()

