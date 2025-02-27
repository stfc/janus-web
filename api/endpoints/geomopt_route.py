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

        print(results)
        results_file_path = results.get("results_path", None)
        traj_path = results.get("traj_path", None)

        if results_file_path:
            with results_file_path.open("rb") as results_file:
                results_content = results_file.read()

        if traj_path:
            with traj_path.open("rb") as traj_file:
                traj_content = traj_file.read()

        return JSONResponse(
            content={
                "results": {
                    k: v
                    for k, v in results.items()
                    if k not in ["results_path", "traj_path"]
                },
                "results_file": {
                    "filename": results_file_path.name,
                    "content": results_content.decode("utf-8"),
                },
                "traj_file": {
                    "filename": traj_path.name,
                    "content": traj_content.decode("utf-8"),
                },
            }
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error - {e}"
        ) from e
