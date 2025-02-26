"""Main module for the application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import geomopt_route, singlepoint_route, upload_route
import logging_config

app = FastAPI()

origins = ["http://localhost", "http://localhost:5173", "http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
)

app.include_router(upload_route.router)
app.include_router(singlepoint_route.router)
app.include_router(geomopt_route.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=8000, log_config=logging_config.LOGGING_CONFIG
    )
