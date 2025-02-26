"""Contains routes for performing geometry optimisation calculations."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.schemas.geomopt_schemas import GeomOptRequest
from api.utils.geomopt_helper import geomopt

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/geomopt", tags=["calculations"])

DATA_DIR = Path("/home/ubuntu/janus-api/janus-web/data")


@router.post("/")
async def get_geomopt(request: GeomOptRequest):
    """
    Endpoint to perform geometry optimisation calculations and return results.

    Parameters
    ----------
    request : GeomOptRequest
        The request body containing the parameters for the calculation.

    Returns
    -------
    dict[str, Any]
        Results of the geometry optimisation calculations.

    Raises
    ------
    HTTPException
        If there is an error during the call.
    """
    base_dir = Path("data")
    struct_path = base_dir / request.struct
    logger.info(f"Request contents: {request}")

    try:
        results = geomopt(struct=struct_path, **request.model_dump(exclude={"struct"}))

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
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error - {e}"
        ) from e
