"""Contains routes for performing singlepoint calculations."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.schemas.singlepoint_schemas import SinglePointRequest
from api.utils.singlepoint_helper import singlepoint

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/singlepoint", tags=["calculations"])

DATA_DIR = Path("/home/ubuntu/janus-api/janus-web/data")


@router.post("/")
async def get_singlepoint(request: SinglePointRequest):
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
    logger.info(f"Request contents: {request}")

    try:
        results = singlepoint(
            struct=struct_path, **request.model_dump(exclude={"struct"})
        )

        results_file_path = results.pop("results_path", None)
        with results_file_path.open("rb") as file:
            file_content = file.read()

        return JSONResponse(
            content={
                "results": results,
                "file": {
                    "filename": results_file_path.name,
                    "content": file_content.decode("utf-8"),
                },
            }
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
