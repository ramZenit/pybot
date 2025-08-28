import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory,file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            print(f"open {target_file}")
            f.write(content)          
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'  
    except Exception as err:
        return f"Error: unable to write to the file: {err}"
