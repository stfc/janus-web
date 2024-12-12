from fastapi import File, UploadFile, Form
from fastapi import APIRouter
from api.utils.upload_helper import save_chunk, reassemble_file

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    chunk_number: int = Form(...),
    total_chunks: int = Form(...)
):  
    # Save the chunk
    chunk_path = save_chunk(await file.read(), chunk_number)
    
    # If all chunks are received, reassemble the file
    if chunk_number == total_chunks:
        complete_file_path = reassemble_file(total_chunks)
        return {"message": "File uploaded successfully", "file_path": complete_file_path}
    
    return {"message": "Chunk uploaded successfully"}