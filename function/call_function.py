from google.genai import types
from function.get_files_info import schema_get_files_info, get_files_info
from function.get_file_content import schema_get_file_content, get_file_content
from function.run_python_file import schema_run_python_file, run_python_file
from function.write_file import schema_write_file, write_file
from config import WORKING_DIRECTORY
available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}") 

    fncts = {
            'get_files_info':get_files_info,
            'get_file_content':get_file_content,
            'run_python_file':run_python_file,
            'write_file':write_file
    }

    if function_call_part.name in fncts:
        # print({**function_call_part.args,'working_directory' : './calculator'})
        fr = fncts[function_call_part.name](**{**function_call_part.args,'working_directory' : WORKING_DIRECTORY})
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": fr},
        )
    ],
)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
        )
    ],
)