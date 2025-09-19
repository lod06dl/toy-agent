import os
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