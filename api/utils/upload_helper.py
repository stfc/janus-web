"""Helper functions for uploading files and accessing uploaded files."""

from __future__ import annotations

import hashlib
from pathlib import Path

DATA_DIR = Path("/home/ubuntu/janus-api/janus-web/data")


def save_chunk(file, chunk_number, original_filename, directory=DATA_DIR):
    """
    Save a chunk of a file to the specified directory.

    Parameters
    ----------
    file : bytes
        The content of the chunk to be saved.
    chunk_number : int
        The number of the chunk being saved.
    original_filename : str
        The original filename of the file being chunked.
    directory : Path, optional
        The directory where the chunk will be saved (default is DATA_DIR).

    Returns
    -------
    str
        The path where the chunk was saved.
    """
    directory.mkdir(parents=True, exist_ok=True)
    chunk_path = directory / f"{original_filename}_chunk_{chunk_number}"
    chunk_path.write_bytes(file)
    return str(chunk_path)


def reassemble_file(total_chunks, original_filename, directory=DATA_DIR):
    """
    Reassemble a file from its chunks.

    Parameters
    ----------
    total_chunks : int
        The total number of chunks.
    original_filename : str
        The original filename of the file being reassembled.
    directory : Path, optional
        The directory where the chunks are stored (default is DATA_DIR).

    Returns
    -------
    str
        The path where the reassembled file was saved.
    """
    output_path = directory / original_filename
    with output_path.open("wb") as complete_file:
        for i in range(total_chunks):
            chunk_path = directory / f"{original_filename}_chunk_{i}"
            with chunk_path.open("rb") as chunk_file:
                complete_file.write(chunk_file.read())
            chunk_path.unlink()
    return str(output_path)


def save_file(file, directory=DATA_DIR):
    """
    Save a file to the specified directory.

    Parameters
    ----------
    file : UploadFile
        The file to be saved.
    directory : Path, optional
        The directory where the file will be saved (default is DATA_DIR).

    Returns
    -------
    str
        The path where the file was saved.
    """
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / file.filename
    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())
    return str(file_path)


def calculate_md5_checksum(file_chunk):
    """
    Calculate the MD5 checksum of a file chunk.

    Parameters
    ----------
    file_chunk : bytes
        The content of the file chunk.

    Returns
    -------
    str
        The MD5 checksum of the file chunk.
    """
    md5 = hashlib.md5()
    md5.update(file_chunk)
    return md5.hexdigest()


def get_all_filenames() -> list[str]:
    """
    Get a list of all filenames in the data directory.

    Returns
    -------
    list of str
        A list of filenames in the data directory.
    """
    filenames = [str(file.name) for file in DATA_DIR.iterdir() if file.is_file()]
    return filenames if filenames else ["No files found"]
