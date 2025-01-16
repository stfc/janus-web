from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import List, Optional, Any, Dict
from api.utils.singplepoint_helper import singlepoint

router = APIRouter(prefix="/singlepoint", tags=["calculations"])

@router.get("/")  
def get_singlepoint(
    struct: str,
    arch: Optional[str] = Query("mace_mp"),
    properties: Optional[List[str]] = Query(None),
    range_selector: Optional[str] = Query(":")
) -> Dict[str, Any]:
    """
    Endpoint to perform single point calculations and return results.
    """
    base_dir = Path("data")
    struct_path = base_dir / struct
    try:
        results = singlepoint(
            struct=struct_path,
            arch=arch,
            properties=properties,
            range_selector=range_selector
        )
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        return results
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")