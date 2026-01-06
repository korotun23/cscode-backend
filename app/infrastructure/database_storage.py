import os
import uuid

# Create working directories if not exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class DatabaseStorage:

    @staticmethod
    def save(file_bytes:bytes) -> str:

        file_id = str(uuid.uuid4())
        path = os.path.join(UPLOAD_DIR, file_id + ".csv")

        try:
            with open(path, "wb") as f:
                f.write(file_bytes)
        except Exception as e:
            raise FileStorageException("Failed to save file: " + str(e))

        return file_id, path

    @staticmethod
    def get_path(file_id: str) -> str:

        path = os.path.join(UPLOAD_DIR, file_id + ".csv")

        if not os.path.exists(path):
            raise FileNotFoundError

        return path
