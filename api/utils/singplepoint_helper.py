from __future__ import annotations

from pathlib import Path
from typing import Any

from janus_core.calculations.single_point import SinglePoint


def singlepoint(
    struct: Path,
    arch: str = "mace_mp",
    properties: list[str] | None = None,
    range_selector: str | None = ":",
) -> dict[str, Any]:
    """
    Perform single point calculations and return results.

    Parameters
    ----------
    struct : Path
        Path of structure to simulate.
    arch : str
        MLIP architecture to use for single point calculations. Default is "mace_mp".
    properties : Optional[List[str]]
        Physical properties to calculate. Default is ("energy", "forces", "stress").
    tracker : bool
        Whether to save carbon emissions of calculation in log file and summary. Default is True.
    range_selector: Optional[str]
        Range of indices to include from the structure. Default is all.

    Returns
    -------
    Dict[str, Any]
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

    return s_point.results


if __name__ == "__main__":
    results = singlepoint(
        struct=Path("../../data/input.data.2055.xyz"),
        range_selector="0:1",
        properties=["stress"],
    )
    print(results)
