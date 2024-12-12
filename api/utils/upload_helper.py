import os

DATA_DIR = "/home/ubuntu/janus-core/app/data"

def save_chunk(file, chunk_number, directory=DATA_DIR):
    os.makedirs(directory, exist_ok=True)
    chunk_path = os.path.join(directory, f"{chunk_number}")
    with open(chunk_path, "wb") as chunk_file:
        chunk_file.write(file)
    return chunk_path

def reassemble_file(total_chunks, directory=DATA_DIR, output_path=os.path.join(DATA_DIR, "complete_file")):
    with open(output_path, "wb") as complete_file:
        for i in range(1, total_chunks + 1):
            chunk_path = os.path.join(directory, f"{i}")
            with open(chunk_path, "rb") as chunk_file:
                complete_file.write(chunk_file.read())
    return output_path
    