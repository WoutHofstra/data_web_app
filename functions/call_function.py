import os
from google import genai
from google.genai import types
from .write_file import *

def call_function(function_call_part):

    functions = {
        "write_file": write_file,
    }

    function_name = function_call_part.name

    if function_name in functions:

        function_to_call = functions[function_name]

        args = function_call_part.args.copy()

        function_result = function_to_call(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )