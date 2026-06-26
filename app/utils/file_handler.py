import os
import io
from config import MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower().strip(".")


def is_valid_file(filename, file_size_bytes):
    extension = get_file_extension(filename)

    if extension not in ALLOWED_EXTENSIONS:
        return False, f"❌ File type '.{extension}' not allowed. Use PDF or TXT."

    file_size_mb = file_size_bytes / (1024 * 1024)

    if file_size_mb > MAX_FILE_SIZE_MB:
        return (
            False,
            f"❌ File too large ({file_size_mb:.1f}MB). Max is {MAX_FILE_SIZE_MB}MB."
        )

    return True, "✅ File is valid."


def read_file_bytes(uploaded_file):
    file_bytes = uploaded_file.read()
    return io.BytesIO(file_bytes)


def get_file_info(uploaded_file):
    uploaded_file.seek(0, 2)
    file_size_bytes = uploaded_file.tell()
    uploaded_file.seek(0)

    is_valid, message = is_valid_file(
        uploaded_file.name,
        file_size_bytes
    )

    return {
        "name": uploaded_file.name,
        "extension": get_file_extension(uploaded_file.name),
        "size_mb": round(file_size_bytes / (1024 * 1024), 2),
        "is_valid": is_valid,
        "message": message
    }