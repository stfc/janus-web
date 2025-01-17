"""Helper functions for uploading files and accessing uploaded files."""

from __future__ import annotations

import hashlib
import os

DATA_DIR = "/home/ubuntu/janus-api/janus-web/data"


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
    directory : str, optional
        The directory where the chunk will be saved (default is DATA_DIR).

    Returns
    -------
    str
        The path where the chunk was saved.
    """
    os.makedirs(directory, exist_ok=True)
    chunk_path = os.path.join(directory, f"{original_filename}_chunk_{chunk_number}")
    with open(chunk_path, "wb") as chunk_file:
        chunk_file.write(file)
    return chunk_path


def reassemble_file(total_chunks, original_filename, directory=DATA_DIR):
    """
    Reassemble a file from its chunks.

    Parameters
    ----------
    total_chunks : int
        The total number of chunks.
    original_filename : str
        The original filename of the file being reassembled.
    directory : str, optional
        The directory where the chunks are stored (default is DATA_DIR).

    Returns
    -------
    str
        The path where the reassembled file was saved.
    """
    output_path = os.path.join(directory, original_filename)
    with open(output_path, "wb") as complete_file:
        for i in range(total_chunks):
            chunk_path = os.path.join(directory, f"{original_filename}_chunk_{i}")
            with open(chunk_path, "rb") as chunk_file:
                complete_file.write(chunk_file.read())
            os.remove(chunk_path)
    return output_path


def save_file(file, directory=DATA_DIR):
    """
    Save a file to the specified directory.

    Parameters
    ----------
    file : UploadFile
        The file to be saved.
    directory : str, optional
        The directory where the file will be saved (default is DATA_DIR).

    Returns
    -------
    str
        The path where the file was saved.
    """
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path


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
    filenames = [
        filename
        for filename in os.listdir(DATA_DIR)
        if os.path.isfile(os.path.join(DATA_DIR, filename))
    ]
    return filenames if filenames else ["No files found"]
