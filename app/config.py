from pydantic import BaseSettings

class Settings (BaseSettings):
    sql_name:str
    user_name:str
    password:str
    host_name:str
    database:str
    secret_key:str
    algorithm:str
    auth_time:int
    db_port:int

    class Config:
        env_file=".env"

settings=Settings()



