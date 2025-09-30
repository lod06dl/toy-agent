import os
from google.genai import types
def write_file(working_directory, file_path, content):

    path2file =os.path.join(working_directory, file_path)
    working_directory = os.path.abspath(working_directory)

    if not os.path.abspath(path2file).startswith(working_directory):
        return  f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(os.path.dirname(path2file)):
        os.makedirs(os.path.dirname(path2file))
        
    with open(path2file, 'w') as file:
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to the given file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            )
        },
    ),
)