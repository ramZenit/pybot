import os
from google.genai import types


def get_files_info(working_directory, directory="."):

    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory,directory))
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    if not target_dir.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


    result = []
    try:
        for filename in os.listdir(target_dir):
            fullpath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(fullpath)
            size = os.path.getsize(fullpath)
            result.append(
                f"- {filename} file_size:{size} bytes, is_dir={is_dir}"
            )
        return "\n".join(result)
    except Exception as err:
        return f"Error: unable to list files: {err}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)