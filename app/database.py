from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote  

SQLALCHEMY_DATABASE_URL = """postgresql://postgres:Muk@2317@Local Postgress/fastapi"""

engine = create_engine("postgresql://postgres:%s@localhost/fastapi" %quote("Muk@2317"))
# note : Here to pass the password , we added %s cause my password contained special characters 
# there is a issue in parsing while creating enginer for db when in any parametric value we have special characters
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
