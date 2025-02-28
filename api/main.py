"""Main module for the application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.constants import FRONTEND_URL, PORT
from api.endpoints import geomopt_route, singlepoint_route, upload_route
import logging_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URL,
    allow_methods=["*"],
)

app.include_router(upload_route.router)
app.include_router(singlepoint_route.router)
app.include_router(geomopt_route.router)

if __name__ == "__main__":
    print(PORT)

    uvicorn.run(
        app, host="0.0.0.0", port=PORT, log_config=logging_config.LOGGING_CONFIG
    )
