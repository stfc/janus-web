"""Helper functions for performing geomotry optimisation calculations."""

from __future__ import annotations

from pathlib import Path

from janus_core.calculations.geom_opt import GeomOpt
from janus_core.helpers.janus_types import Architectures

from api.schemas.geomopt_schemas import GeomOptResults
from api.utils.data_conversion_helper import convert_ndarray_to_list

DATA_DIR = Path("/home/ubuntu/janus-api/janus-web/data")


def geomopt(
    struct: Path,
    arch: Architectures | None = "mace_mp",
    fmax: float = 0.1,
    steps: int = 1000,
    write_results: bool | None = True,
    results_path: Path | None = DATA_DIR / "results/",
    format: str | None = "cif",
) -> GeomOptResults:
    """
    Perform geometry optimisation and return results.

    Parameters
    ----------
    struct : Path
        Path of structure to optimise.
    arch : Architectures
        MLIP architecture to use for geometry optimisation. Default is "mace_mp".
    fmax : float
        Force convergence criteria for the optimiser, by default 0.1 eV/Å.
    steps : int
        Maximum number of optimisation steps, by default 1000.
    write_results : bool | None, default is True
        Tells function if to save the results of the calculation or not.
    results_path : Path | None
        Location to save the results.
    format : str
        File format to output results as.

    Returns
    -------
    GeomOptResults
        Results of the geometry optimisation.
    """
    read_kwargs = {"index": ":"}
    results_path = results_path / f"{struct.stem}-results.{format}"
    write_kwargs = {"filename": results_path, "format": f"{format}"}

    geomopt_kwargs = {
        "struct_path": struct,
        "arch": arch,
        "device": "cpu",
        "fmax": fmax,
        "steps": steps,
        "read_kwargs": read_kwargs,
        "write_results": write_results,
        "write_kwargs": write_kwargs,
    }

    geom_opt = GeomOpt(**geomopt_kwargs)

    geom_opt.run()
    results = convert_ndarray_to_list(geom_opt.struct.info)
    results["results_path"] = results_path

    return results


if __name__ == "__main__":
    struct_path = DATA_DIR / "NaCl-single.xyz"
    optimised_results = geomopt(struct_path)

    print(optimised_results)
