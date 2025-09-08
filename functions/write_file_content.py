import os
from google.genai import types

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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file from a specified file path with the specified content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)