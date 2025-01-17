from __future__ import annotations

from fastapi import FastAPI

from api.endpoints import  upload_route

app = FastAPI()

app.include_router(upload_route.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)