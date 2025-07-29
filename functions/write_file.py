# functions/write_file.py

import os

def write_file(working_directory, file_path, content):
    # If the file path is outside of the directory, return a string with error
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not full_path.startswith(working_directory):
        return(f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory")

    if os.path.isdir(full_path):
        return f"Error: Cannot write to '{file_path}' because a directory with that name already exists"

    parent_dir = os.path.dirname(full_path)
    try:
        os.makedirs(parent_dir, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return(f"Successfully wrote to '{file_path}' ({len(content)}) characters written") 
    except Exception as e:
        return(f"Error: Writing to {file_path} failed.  {e}")