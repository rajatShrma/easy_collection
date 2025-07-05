from fastapi import FastAPI
from database import create_db_and_tables
from routers import user

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user.router)
