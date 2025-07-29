# functions/get_file_content.py

import os
from constants import MAX_CHARS

def get_file_content(working_directory, file_path):
    # Ensure the file_path is within working_directory
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(working_directory):
        return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
    
    # Ensure the file_path if not a file
    if not os.path.isfile(full_path):
        return f"Error: File not found or is not a regular file: {file_path}"

    # Read file
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
        return file_content_string
    except FileNotFoundError:
        return(f"Error: The file {file_path} was not found")
    except PermissionError:
        return(f"Error: Permission denied when trying to read {file_path}")
    except OSError as e:
        return(f"Error: Reading file '{file_path}' : {e}")