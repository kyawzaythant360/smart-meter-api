from fastapi import FastAPI
from app.routes import router
from app.demo_data import insert_demo_data

app = FastAPI(title="Generator Usage API")

app.include_router(router)

@app.on_event("startup")
async def startup():
    await insert_demo_data()
