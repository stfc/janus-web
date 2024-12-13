from fastapi import APIRouter, UploadFile, File, HTTPException
from api.utils.upload_helper import save_chunk, reassemble_file, save_file

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/chunk")
async def upload_chunk(file: UploadFile = File(...), chunk_number: int = 0, total_chunks: int = 1):
    print("chunk")
    try:
        chunk_path = save_chunk(await file.read(), chunk_number, file.filename)
        if chunk_number == total_chunks:
            reassemble_file(total_chunks, file.filename)
        return {"message": "Chunk uploaded successfully", "chunk_path": chunk_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/single")
async def upload_single(file: UploadFile = File(...)):
    print("single")
    try:
        file_path = save_file(file)
        return {"message": "File uploaded successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))