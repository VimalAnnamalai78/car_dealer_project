from fastapi import FastAPI
import uvicorn
from database import models
from database.connection_db import engine
from routers import cars, login, dealers

app = FastAPI()
models.Base.metadata.create_all(engine)
origins = ["http://localhost:8000"]

app.include_router(cars.router, prefix="/cars")
app.include_router(dealers.router, prefix="/dealer")
app.include_router(login.router, prefix="/login", tags=['Login Authentication'])

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload=True)
    print("======CAR DEALER SERVER STARTED=========")
