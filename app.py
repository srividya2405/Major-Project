from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="FinGuard AML API",
    description="Real-Time AML & Fraud Detection System",
    version="1.0"
)

app.include_router(router)


@app.get("/")
async def home():

    return {

        "message": "Welcome to FinGuard AML API"

    }