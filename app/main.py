import os

from api import router
from fastapi import FastAPI

app = FastAPI(title="Resume AI coach", version="0.1")


@app.on_event("startup")
async def startup_event():
    if os.environ.get("TEST_MODE") != "1":
        from pipeline import warmup_models

        await warmup_models()


app.include_router(router)
