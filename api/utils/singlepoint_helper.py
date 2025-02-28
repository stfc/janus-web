"""Helper functions for performing singeploint calculations."""

from __future__ import annotations

import logging
from pathlib import Path

from janus_core.calculations.single_point import SinglePoint
from janus_core.helpers.janus_types import Architectures, Properties

from api.constants import DATA_DIR
from api.schemas.singlepoint_schemas import SinglePointResults
from api.utils.data_conversion_helper import convert_ndarray_to_list

logger = logging.getLogger(__name__)


def singlepoint(
    struct: Path,
    arch: Architectures | None = "mace_mp",
    properties: list[Properties] | None = None,
    range_selector: str | None = ":",
    write_results: bool | None = True,
    results_path: Path | None = DATA_DIR,
    format: str | None = "extxyz",
) -> SinglePointResults:
    """
    Perform single point calculations and return results.

    Parameters
    ----------
    struct : Path
        Path of structure to simulate.
    arch : Architectures
        MLIP architecture to use for single point calculations. Default is "mace_mp".
    properties : List[Properties]
        Physical properties to calculate. Default is ("energy", "forces", "stress").
    range_selector : str
        Range of indices to include from the structure. Default is all.
    write_results : bool | None, default is True
        Tells function if to save the results of the calculation or not.
    results_path : Path | None
        Location to save the results.
    format : str
        File format to output results as.

    Returns
    -------
    dict[str, Any]
        Results of the single point calculations.
    """
    logger.info(f"format type: {format}")
    read_kwargs = {"index": range_selector}
    results_path = results_path / f"{struct.stem}-results.{format}"
    write_kwargs = {"filename": results_path, "format": f"{format}"}

    singlepoint_kwargs = {
        "struct_path": struct,
        "properties": properties,
        "arch": arch,
        "device": "cpu",
        "read_kwargs": read_kwargs,
        "write_results": write_results,
        "write_kwargs": write_kwargs,
    }

    s_point = SinglePoint(**singlepoint_kwargs)

    s_point.run()
    results = convert_ndarray_to_list(s_point.results)
    results["results_path"] = results_path

    return results
