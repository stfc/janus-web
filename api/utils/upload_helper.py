import os

DATA_DIR = "/home/ubuntu/janus-core/app/data"

def save_chunk(file, chunk_number, original_filename, directory=DATA_DIR):
    os.makedirs(directory, exist_ok=True)
    chunk_path = os.path.join(directory, f"{original_filename}_chunk_{chunk_number}")
    with open(chunk_path, "wb") as chunk_file:
        chunk_file.write(file)
    return chunk_path

def reassemble_file(total_chunks, original_filename, directory=DATA_DIR):
    output_path = os.path.join(directory, original_filename)
    with open(output_path, "wb") as complete_file:
        for i in range(1, total_chunks + 1):
            chunk_path = os.path.join(directory, f"{original_filename}_chunk_{i}")
            with open(chunk_path, "rb") as chunk_file:
                complete_file.write(chunk_file.read())
    return output_path

def save_file(file, directory=DATA_DIR):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path