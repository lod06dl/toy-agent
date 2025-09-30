from config import MAX_FILE_LENGHT
import os
from google.genai import types
def get_file_content(working_directory, file_path):
    path2file =os.path.join(working_directory, file_path)

    working_directory = os.path.abspath(working_directory)

    if not os.path.exists(path2file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not os.path.isfile(path2file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not os.path.abspath(path2file).startswith(working_directory):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(path2file) as file:
        content = file.read()
        if len(content) > MAX_FILE_LENGHT:
            return content[:MAX_FILE_LENGHT]+'[...File "{file_path}" truncated at {MAX_FILE_LENGHT} characters]'
        else:
            return content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file, constrained to the working directory. If the file is too large, it will be truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the content of, relative to the working directory.",
            ),
        },
    ),
)