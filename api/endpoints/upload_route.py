from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from api.utils.upload_helper import save_chunk, reassemble_file, save_file, calculate_md5_checksum, get_all_filenames

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/chunk")
async def upload_chunk(
                       file: UploadFile = File(...),
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

@router.post("/single")
async def upload_single(file: UploadFile = File(...), file_hash: str = Form(...)):
    print(f"Received File MD5 Hash:   {file_hash}")
    try:
        file_content = await file.read()
        calculated_hash = calculate_md5_checksum(file_content)
        print(f"Calculated File MD5 Hash: {calculated_hash}")
        print(f"Hash matches: {calculated_hash == file_hash}")

        file_path = save_file(file)
        return {"message": "File uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/files")
async def get_files() -> list(str):
    filenames = [filename for filename in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, filename))]
    return filenames if filenames else ["No files found"]