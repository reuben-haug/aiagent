# functions/run_python.py

import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    # Ensure the file_path is within working_directory
    working_directory = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_path):
        return f'Error: File "{file_path}" not found'
    
    if not full_path.endswith(".py"):
        return f"Error: '{file_path}' is not a Python file"
    
    # Build command list
    command = ["python", full_path] + args

    try:
        completed_process = subprocess.run(
            command, 
            timeout=30, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=working_directory,
            text=True
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        if not stdout and not stderr:
            return "No output produced"
        
        output = ""
        if stdout:
            output += f"STDOUT: {stdout}"
        if stderr:
            output += f"STDERR: {stderr}"
        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}"
        
        return output.strip()
    
    except Exception as e:
        return f"Error: executing Python file: {e}"