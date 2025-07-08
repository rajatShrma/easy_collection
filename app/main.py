from fastapi import FastAPI
from database import create_db_and_tables
from routers import user
from routers import brand
from routers import product
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user.router)
app.include_router(brand.router)
app.include_router(product.router)