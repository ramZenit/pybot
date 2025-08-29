import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    if not file_path.split(".")[-1] == "py":
        return f'Error: "{file_path}" is not a Python file.'
    
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    try:
        command = ["python", target_file] 
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            command, 
            timeout=30, 
            capture_output=True,     
            text=True,               
            cwd=abs_working_directory
            )

        if completed_process.check_returncode():
            return f"Process exited with code {completed_process.returncode}" 
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced"

        return f"STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr if completed_process.stderr else None}"
    
    except Exception as err:
        return f"Error: executing Python file: {err}"    