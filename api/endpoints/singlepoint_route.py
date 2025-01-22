"""Contains routes for performing singlepoint calculations."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query

from api.utils.singlepoint_helper import singlepoint

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/singlepoint", tags=["calculations"])


@router.get("/")
def get_singlepoint(
    struct: Annotated[str, Query()],
    arch: Annotated[str | None, Query("mace_mp")],
    properties: Annotated[list[str] | None, Query(None)],
    range_selector: Annotated[str | None, Query(":")],
) -> dict[str, Any]:
    """
    Endpoint to perform single point calculations and return results.

    Parameters
    ----------
    struct : str
        The filename of the dataset to perform calculations on.
    arch : str
        The name of the model to perform the calculations with.
    properties : List[str]
        The properties to calculate.
    range_selector : str
        The range of indicies to read from the data structure.

    Returns
    -------
    Dict[str, Any]
        Results of the single point calculations.

    Raises
    ------
    HTTPException
        If there is an error during the call.
    """
    base_dir = Path("data")
    struct_path = base_dir / struct
    try:
        results = singlepoint(
            struct=struct_path,
            arch=arch,
            properties=properties,
            range_selector=range_selector,
        )
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        return results
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
