import os
from config import CHARACTER_LIMIT
from google.genai import types


def get_file_content(working_directory, file_path):

    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory,file_path))

    if not target_file.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            content = f.read(CHARACTER_LIMIT)            
            if os.path.getsize(target_file) > CHARACTER_LIMIT:
                content += (
                    f'[...File "{file_path} truncated at {CHARACTER_LIMIT} characters]'
                )                
        return content
    except Exception as err:
        return f"Error: unable to read the file: {err}"



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {CHARACTER_LIMIT} characters of the content form a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"]
    ),
)