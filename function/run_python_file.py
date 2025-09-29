import os
import subprocess
from config import TIMEOUT
import sys
def run_python_file(working_directory, file_path, args=[]):
    path2file =os.path.join(working_directory, file_path)
    working_directory = os.path.abspath(working_directory)

    if not os.path.exists(path2file):
        return f'Error: File "{file_path}" not found.'
    if not os.path.abspath(path2file).startswith(working_directory):
       return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not path2file.endswith(".py"):
        return f'Error: File "{file_path}" is not a Python file.'

    try:
        result  = subprocess.run([sys.executable, file_path, *args], cwd=working_directory, capture_output=True, text=True ,timeout=TIMEOUT)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    if result.returncode == 0:
       return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nThe "completed_process" object has a stdout and stderr attribute.' 
    elif result.returncode != 0:
       return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nThe "completed_process" object has a stdout and stderr attribute.\nProcess exited with code {result.returncode}.'
    elif result is None: 
        "No output produced."

#    Return a string with the output formatted to include:
# The stdout prefixed with STDOUT:, and stderr prefixed with STDERR:. .
# If the process exits with a non-zero code, include "Process exited with code X"
# If no output is produced, return "No output produced."
# If any exceptions occur during execution, catch them and return an error string: