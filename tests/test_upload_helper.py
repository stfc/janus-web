"""Tests for the upload helper functions."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shutil

import pytest

from api.utils.upload_helper import (
    calculate_md5_checksum,
    get_all_filenames,
    reassemble_file,
    save_chunk,
    save_file,
)

DATA_DIR = Path("/home/ubuntu/janus-api/janus-web/data")


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Create a temporary directory for testing."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(DATA_DIR)


def test_save_chunk():
    """Test if save chunk function saves a given chunk in the correct directory."""
    file_chunk = b"Test chunk data"
    chunk_number = 0
    original_filename = "testfile.txt"

    chunk_path = save_chunk(file_chunk, chunk_number, original_filename)

    assert Path(chunk_path).exists()
    assert Path(chunk_path).read_bytes() == file_chunk


def test_reassemble_file():
    """Test if file is correctly rebuilt when function called."""
    original_filename = "testfile.txt"
    total_chunks = 2
    file_chunks = [b"Test chunk 1", b"Test chunk 2"]

    for i, chunk in enumerate(file_chunks):
        save_chunk(chunk, i, original_filename)

    reassembled_file_path = reassemble_file(total_chunks, original_filename)

    assert Path(reassembled_file_path).exists()
    assert Path(reassembled_file_path).read_bytes() == b"".join(file_chunks)


def test_save_file(tmp_path):
    """Test if save file function saves a given file in the correct directory."""
    from io import BytesIO

    from fastapi import UploadFile

    file_content = b"Test file content"
    file = UploadFile(filename="testfile.txt", file=BytesIO(file_content))

    file_path = save_file(file, directory=tmp_path)

    assert Path(file_path).exists()
    assert Path(file_path).read_bytes() == file_content


def test_get_all_filenames():
    """Test if getter returns all of the filenames correctly."""
    filenames = ["file1.txt", "file2.txt"]
    for filename in filenames:
        (DATA_DIR / filename).write_text("Test content")

    result = get_all_filenames()

    assert sorted(result) == sorted(filenames)


def test_calculate_md5_checksum():
    """Test for checksum check when the hash should match."""
    file_chunk = b"Test data for checksum"
    received_hash = hashlib.md5(file_chunk).hexdigest()
    result = calculate_md5_checksum(file_chunk, received_hash)

    assert result


def test_calculate_md5_checksum_mismatch():
    """Test for checksum check when the hash is incorrect."""
    file_chunk = b"Test data for checksum"
    received_hash = "incorrecthash"
    result = calculate_md5_checksum(file_chunk, received_hash)

    assert not result