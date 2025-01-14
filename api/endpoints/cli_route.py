from __future__ import annotations

from fastapi import APIRouter

from api.utils.cli_helper import show_options

router = APIRouter(prefix="/cli", tags=["cli"])


@router.get("")
async def get_options():
    return show_options()
