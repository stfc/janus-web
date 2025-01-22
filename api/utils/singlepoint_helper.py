"""Helper functions for performing singeploint calculations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from janus_core.calculations.single_point import SinglePoint
import numpy as np


def singlepoint(
    struct: Path,
    arch: str | None = "mace_mp",
    properties: list[str] | None = None,
    range_selector: str | None = ":",
) -> dict[str, Any]:
    """
    Perform single point calculations and return results.

    Parameters
    ----------
    struct : str
        Filename of structure to simulate.
    arch : str
        MLIP architecture to use for single point calculations. Default is "mace_mp".
    properties : List[str]
        Physical properties to calculate. Default is ("energy", "forces", "stress").
    range_selector : str
        Range of indices to include from the structure. Default is all.

    Returns
    -------
    Dict[str, Any]
        Results of the single point calculations.
    """
    read_kwargs = {"index": range_selector}
    if properties == "all properties":
        properties = None

    singlepoint_kwargs = {
        "struct_path": struct,
        "properties": properties,
        "arch": arch,
        "device": "cpu",
        "read_kwargs": read_kwargs,
    }
    print(singlepoint_kwargs)

    s_point = SinglePoint(**singlepoint_kwargs)

    s_point.run()

    results = s_point.results

    # Convert numpy arrays to lists
    for key, value in results.items():
        if isinstance(value, np.ndarray):
            results[key] = value.tolist()

    return results


if __name__ == "__main__":
    results = singlepoint(
        struct=Path("janus-web/data/input.data.2055.xyz"),
        range_selector="0:1",
        properties=["stress"],
    )
    print(results)
