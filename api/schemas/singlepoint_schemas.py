"""Schemas for singlepoint calculation functions."""

from __future__ import annotations

from pathlib import Path

from janus_core.helpers.janus_types import Architectures, Properties
from pydantic import BaseModel


class SinglePointResults(BaseModel):
    """Class validation for singlepoint results."""

    results_path: Path | None
    forces: Properties | None
    energy: Properties | None
    stress: Properties | None
    hessian: Properties | None


class SinglePointRequest(BaseModel):
    """Class validation for singlepoint requests."""

    struct: str
    arch: Architectures | None = "mace_mp"
    properties: list[Properties] | None = None
    range_selector: str | None = None
    format: str | None = "extxyz"
