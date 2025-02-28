"""Helper functions for uploading files and accessing uploaded files."""

from __future__ import annotations

import hashlib
from pathlib import Path

from api.constants import DATA_DIR


def save_file(file_contents: bytes, filename: str, directory: Path = DATA_DIR):
    """
    Save a file to the specified directory.

    Parameters
    ----------
    file_contents : bytes
        The file to be saved.
    filename : str
        Name of the file to be saved.
    directory : Path, optional
        The directory where the file will be saved (default is DATA_DIR).

    Returns
    -------
    str
        The path where the file was saved.
    """
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / filename
    file_path.write_bytes(file_contents)
    return file_path


def calculate_md5_checksum(file_chunk: bytes, received_hash: str) -> bool:
    """
    Calculate the MD5 checksum of a file chunk.

    Parameters
    ----------
    file_chunk : bytes
        The content of the file chunk.
    received_hash : str
        The hash calculated before the file was uploaded.

    Returns
    -------
    bool
        True if the hash matches.
    """
    md5 = hashlib.md5()
    md5.update(file_chunk)
    calculated_hash = md5.hexdigest()
    return calculated_hash == received_hash


def get_all_filenames(directory: Path = DATA_DIR) -> list[str]:
    """
    Get a list of all filenames in the data directory.

    Parameters
    ----------
    directory : Path
        Directory to get the filenames from.

    Returns
    -------
    list of str
        A list of filenames in the data directory.
    """
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    filenames = [str(file.name) for file in directory.iterdir() if file.is_file()]
    return filenames if filenames else []
