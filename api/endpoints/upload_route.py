"""Contains routes for uploading files and accessing uploaded files."""

from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from api.utils.upload_helper import (
    calculate_md5_checksum,
    get_all_filenames,
    reassemble_file,
    save_chunk,
    save_file,
)

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/chunk")
async def upload_chunk(
    file: UploadFile = None,
    chunk_number: int = Form(...),
    total_chunks: int = Form(...),
    chunk_hash: str = Form(...),
):
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

    Returns
    -------
    dict
        A dictionary containing a message and the path where the chunk was saved.

    Raises
    ------
    HTTPException
        If there is an error during the upload process.
    """
    if file is None:
        file = File(...)
    print(file.filename)
    print(f"Received chunk {chunk_number} of {total_chunks}")
    print(f"Received Chunk MD5 Hash:   {chunk_hash}")
    try:
        file_content = await file.read()
        calculated_hash = calculate_md5_checksum(file_content)
        print(f"Calculated Chunk MD5 Hash: {calculated_hash}")
        print(f"Hash matches: {calculated_hash == chunk_hash}")

        chunk_path = save_chunk(file_content, chunk_number, file.filename)
        print(f"Chunk saved at: {chunk_path}")

        if chunk_number == total_chunks - 1:
            reassemble_file(total_chunks, file.filename)
        return {"message": "Chunk uploaded successfully", "chunk_path": chunk_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/single")
async def upload_single(file: UploadFile = None, file_hash: str = Form(...)):
    """
    Upload a single file.

    Parameters
    ----------
    file : UploadFile
        The file to be uploaded.
    file_hash : str
        The MD5 hash of the file.

    Returns
    -------
    dict
        A dictionary containing a message and the path where the file was saved.

    Raises
    ------
    HTTPException
        If there is an error during the upload process.
    """
    if file is None:
        file = File(...)
    print(f"Received File MD5 Hash:   {file_hash}")
    try:
        file_content = await file.read()
        calculated_hash = calculate_md5_checksum(file_content)
        print(f"Calculated File MD5 Hash: {calculated_hash}")
        print(f"Hash matches: {calculated_hash == file_hash}")

        file_path = save_file(file)
        return {"message": "File uploaded successfully", "file_path": file_path}
    except Exception as e:
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
