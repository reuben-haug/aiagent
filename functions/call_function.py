# functions/call_function.py

from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from schema_definitions import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from constants import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)


def call_function(function_call_part, verbose=False):
    '''
    Handles task calling.  Calls the specified function and captures the result.
    
    'function_call_part is a 'types.FunctionCall' object that has name and argument properties.
    '''
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
    }

    function_name = function_call_part.name

     # Call the specified function
    if function_name not in func_dict:
        # Return Content object indicating unknown function
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ],
        )
    else:
        # Manually add the working directory from 'constants.py'
        args = dict(function_call_part.args)
        args["working_directory"] = WORKING_DIR

        function_result = func_dict[function_name](**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result}
                )
            ],
        )