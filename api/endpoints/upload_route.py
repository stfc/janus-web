"""Contains routes for uploading files and accessing uploaded files."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from api.utils.upload_helper import (
    calculate_md5_checksum,
    get_all_filenames,
    reassemble_file,
    save_chunk,
    save_file,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/chunk")
async def upload_chunk(
    file: Annotated[UploadFile, File()],
    chunk_number: Annotated[int, Form()],
    total_chunks: Annotated[int, Form()],
    chunk_hash: Annotated[str, Form()],
) -> None:
    """
    Allow individual chunks to be uploaded and later reassembled.

    Parameters
    ----------
    file : UploadFile
        The chunk file to be uploaded.
    chunk_number : int
        The number of the chunk being uploaded.
    total_chunks : int
        The total number of chunks for the file.
    chunk_hash : str
        The MD5 hash of the chunk.

    Raises
    ------
    HTTPException
        If there is an error during the upload process.
    """
    logger.info(f"Received chunk {chunk_number} of {total_chunks}")
    try:
        file_content = await file.read()
        hash_match = calculate_md5_checksum(file_content, chunk_hash)
        logger.info(f"Hash matches: {hash_match}")

        save_chunk(file_content, chunk_number, file.filename)

        if chunk_number == total_chunks - 1:
            reassemble_file(total_chunks, file.filename)
    except Exception as e:
        logger.error(f"Error during chunk upload: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/single")
async def upload_single(
    file: Annotated[UploadFile, File()],
    file_hash: Annotated[str, Form()],
) -> None:
    """
    Upload a single file.

    Parameters
    ----------
    file : UploadFile
        The file to be uploaded.
    file_hash : str
        The MD5 hash of the file.

    Raises
    ------
    HTTPException
        If there is an error during the upload process.
    """
    try:
        file_content = await file.read()
        logger.info(f"Hash matches: {calculate_md5_checksum(file_content, file_hash)}")

        save_file(file)
    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/files")
async def get_files() -> list[str]:
    """
    Get a list of all uploaded files.

    Returns
    -------
    list of str
        A list of filenames of all uploaded files.
    """
    return get_all_filenames()
