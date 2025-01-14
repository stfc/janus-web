import os
import hashlib

DATA_DIR = "/home/ubuntu/janus-api/janus-web/data"

def save_chunk(file, chunk_number, original_filename, directory=DATA_DIR):
    os.makedirs(directory, exist_ok=True)
    chunk_path = os.path.join(directory, f"{original_filename}_chunk_{chunk_number}")
    with open(chunk_path, "wb") as chunk_file:
        chunk_file.write(file)
    return chunk_path

def reassemble_file(total_chunks, original_filename, directory=DATA_DIR):
    output_path = os.path.join(directory, original_filename)
    with open(output_path, "wb") as complete_file:
        for i in range(total_chunks):
            chunk_path = os.path.join(directory, f"{original_filename}_chunk_{i}")
            with open(chunk_path, "rb") as chunk_file:
                complete_file.write(chunk_file.read())
            os.remove(chunk_path)
    return output_path

def save_file(file, directory=DATA_DIR):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path

def calculate_md5_checksum(file_chunk):
    md5 = hashlib.md5()
    md5.update(file_chunk)
    return md5.hexdigest()

def get_all_filenames() -> list[str]:
    filenames = [filename for filename in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, filename))]
    return filenames if filenames else ["No files found"]