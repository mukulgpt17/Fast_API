from fastapi import FastAPI
from .routers import post,user,auth,vote
from .database import engine
from . import models

# # this is used to create all the tables in the db
models.Base.metadata.create_all(bind=engine)  # as we are now using alembic , its not relevant 
from fastapi.middleware.cors import CORSMiddleware


origins = ["*"]


app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"Welcome to main page"}

# to run the app in the termain head to app directory 
# run uvicorn main:app --reload (--reload is used if any changes are done it auto restarts the server )

