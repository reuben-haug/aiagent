# functions/get_files_info.py

import os

def get_files_info(working_directory, directory=None):
    # Resolve the target directory
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    else:
        target_dir = os.path.abspath(working_directory)

    # Ensure the target_dir is within working_directory
    working_directory = os.path.abspath(working_directory)
    if not os.path.commonpath([working_directory, target_dir]) == working_directory:
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    if not os.path.isdir(target_dir):
        return f"Error: '{directory or working_directory}' is not a valid directory"

    lines = []
    for root, dirs, files in os.walk(target_dir):
        for name in files + dirs:
            entry_path = os.path.join(root, name)
            rel_path = os.path.relpath(entry_path, working_directory)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                lines.append(f"- {rel_path}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                lines.append(f"{rel_path}: Error reading entry: {e}")
    return '\n'.join(lines)