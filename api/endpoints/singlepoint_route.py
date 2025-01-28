"""Contains routes for performing singlepoint calculations."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from janus_core.helpers.janus_types import Architectures, Properties
from pydantic import BaseModel

from api.utils.singlepoint_helper import singlepoint

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/singlepoint", tags=["calculations"])


class SinglePointRequest(BaseModel):
    """Class validation for singlepoint requests."""

    struct: str
    arch: Architectures
    properties: list[Properties]
    range_selector: str


@router.post("/")
def get_singlepoint(request: SinglePointRequest) -> dict[str, Any]:
    """
    Endpoint to perform single point calculations and return results.

    Parameters
    ----------
    request : SinglePointRequest
        The request body containing the parameters for the calculation.

    Returns
    -------
    dict[str, Any]
        Results of the single point calculations.

    Raises
    ------
    HTTPException
        If there is an error during the call.
    """
    base_dir = Path("data")
    struct_path = base_dir / request.struct
    logger.info(request)
    try:
        results = singlepoint(
            struct=struct_path,
            arch=request.arch,
            properties=request.properties,
            range_selector=request.range_selector,
        )
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        return results
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
