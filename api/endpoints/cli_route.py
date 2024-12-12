from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from api.utils.cli_helper import show_options

router = APIRouter(prefix="/cli", tags=["cli"])

@router.get("")
async def get_options():
    return show_options()