import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    path =os.path.join(working_directory, directory)

    working_directory = os.path.abspath(working_directory)

    if  not os.path.exists(path):
        return f'Error: "{directory}" is not a directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    if not os.path.abspath(path).startswith(working_directory):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    return '\n'.join([f'- {file}: filesize={os.path.getsize(os.path.join(path, file))}, is_dir={os.path.isdir(os.path.join(path, file))}' for file in os.listdir(path)])

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