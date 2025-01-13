from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from api.utils.singlepoint_helper import singlepoint

router = APIRouter(prefix="/singlepoint", tags=["calculations"])

@router.post("/")
async def calculate_singlepoint(
                       filename: str,
                       chunk_number: int = Form(...),
                       total_chunks: int = Form(...),
                       chunk_hash: str = Form(...)):
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
        raise HTTPException(status_code=500, detail=str(e))