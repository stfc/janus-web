"""Helper functions for performing data conversion."""

from __future__ import annotations

from typing import Any

import numpy as np


def convert_ndarray_to_list(
    data: dict[str, Any] | list | np.ndarray | float,
) -> dict[str, Any]:
    """
    Recursive function to convert numpy arrays into a usable format for fastAPI.

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
