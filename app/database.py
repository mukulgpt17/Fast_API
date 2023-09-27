from sqlalchemy import create_engine,URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#https://docs.sqlalchemy.org/en/20/core/engines.html
#note if password has special characters or any other attributes please use URL object to create object of the same 
#pass this URL object in the create_engine 

url_object=URL.create(
    settings.sql_name,
    username=settings.user_name,
    password=settings.password,
    host=settings.host_name,
    port=settings.db_port,
    database=settings.database
)

engine=create_engine(url_object)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# intiates the session for sql alchemy -> DB 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Direct connection to the SQL DB 
# #direct DB connection 
# while True:
#     try : 
#         conn=psycopg2.connect(host='localhost',database='Database_Name',user ='user_name'
#                             ,password='user_password',cursor_factory=RealDictCursor )
#         cursor=conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as err:
#         print("Connecting to database failed")
#         print("error",err)
#         time.sleep(2)