from fastapi import FastAPI
from routers import post,user


app= FastAPI()
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"Welcome to main page"}


# to run the app in the termain head to app directory 
# run uvicorn main:app --reload (--reload is used if any changes are done it auto restarts the server )

