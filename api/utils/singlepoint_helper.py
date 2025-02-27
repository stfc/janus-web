"""Helper functions for performing singeploint calculations."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from janus_core.calculations.single_point import SinglePoint
from janus_core.helpers.janus_types import Architectures, Properties
import numpy as np

logger = logging.getLogger(__name__)


def convert_ndarray_to_list(
    data: dict[str, Any] | list | np.ndarray | float,
) -> dict[str, Any]:
    """
    Recursive function to convert numpy arrays into a useable format for fastAPI.

    Parameters
    ----------
    data : dict[str, Any] | list | np.ndarray | float
        The object to be checked and potentially converted.

    Returns
    -------
    dict[str, Any]
        Dictionary of properties calculated.
    """
    if isinstance(data, np.ndarray):
        return data.tolist()
    if isinstance(data, dict):
        return {k: convert_ndarray_to_list(v) for k, v in data.items()}
    if isinstance(data, list):
        return [convert_ndarray_to_list(i) for i in data]
    return data


def singlepoint(
    struct: Path,
    arch: Architectures | None = "mace_mp",
    properties: list[Properties] | None = None,
    range_selector: str | None = ":",
) -> dict[str, Any]:
    """
    Perform single point calculations and return results.

    Parameters
    ----------
    struct : str
        Filename of structure to simulate.
    arch : Architectures
        MLIP architecture to use for single point calculations. Default is "mace_mp".
    properties : List[Properties]
        Physical properties to calculate. Default is ("energy", "forces", "stress").
    range_selector : str
        Range of indices to include from the structure. Default is all.

    Returns
    -------
    dict[str, Any]
        Results of the single point calculations.
    """
    read_kwargs = {"index": range_selector}

    singlepoint_kwargs = {
        "struct_path": struct,
        "properties": properties,
        "arch": arch,
        "device": "cpu",
        "read_kwargs": read_kwargs,
    }

    s_point = SinglePoint(**singlepoint_kwargs)

    s_point.run()

    return convert_ndarray_to_list(s_point.results)
