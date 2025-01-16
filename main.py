from __future__ import annotations

from fastapi import FastAPI

from api.endpoints import cli_route, upload_route, singlepoint_route

app = FastAPI()

app.include_router(cli_route.router)
app.include_router(upload_route.router)
app.include_router(singlepoint_route.router)


@app.get("/")
def read_root():
    return {"Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
