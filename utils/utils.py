import os

def is_file_of_format(file_path, file_formats):
    if not os.path.isfile(file_path):
        return False

    _, ext = os.path.splitext(file_path)

    if ext.lower() == file_formats:
        return True
    
    return False
